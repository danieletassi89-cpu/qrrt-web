#!/usr/bin/env python3
"""Importatore prototipo TASSIUFFICIO per esportazioni ufficiali OD+.

Legge un file esportato dal portale (CSV o XLSX), lo normalizza secondo
config/mappatura_colonne.json, applica i ricarichi di config/ricarichi.csv
e scrive dati/campione_normalizzato.csv e .json.

Regole:
- un dato mancante resta vuoto, non viene mai stimato o inventato;
- nessuna conversione pezzo/confezione: il prezzo resta com'è nel file;
- nessun accesso di rete e nessuna credenziale.

Uso:
    python importatore/importa.py dati/originali/<file> [--cliente CODICE] [--confronto]
"""
import argparse
import csv
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CAMPI = [
    "codice_od", "ean", "cod_produttore", "nome", "descrizione", "marca",
    "categoria", "immagine_url", "prezzo_acquisto_netto", "valuta", "iva_pct",
    "unita_vendita", "pezzi_per_confezione", "qta_minima", "giacenza",
    "tempo_approvvigionamento", "data_aggiornamento",
]
CAMPI_DECIMALI = {"prezzo_acquisto_netto", "iva_pct"}
CAMPI_INTERI = {"pezzi_per_confezione", "qta_minima"}
# giacenza non e' tra gli interi: il portale potrebbe esporre "disponibile"
# invece di una quantita', e va conservato cosi' com'e'.


def carica_mappatura(percorso):
    with open(percorso, encoding="utf-8") as f:
        return json.load(f)


def leggi_righe(percorso, mappatura):
    if percorso.suffix.lower() in (".xlsx", ".xlsm"):
        try:
            import openpyxl
        except ImportError:
            sys.exit("Per i file Excel serve openpyxl: pip install openpyxl")
        foglio = openpyxl.load_workbook(percorso, read_only=True, data_only=True).active
        righe = list(foglio.iter_rows(values_only=True))
        intestazioni = [str(c).strip() if c is not None else "" for c in righe[0]]
        return [
            {h: ("" if v is None else str(v)) for h, v in zip(intestazioni, r)}
            for r in righe[1:]
        ]
    with open(percorso, encoding=mappatura.get("codifica", "utf-8-sig"), newline="") as f:
        return list(csv.DictReader(f, delimiter=mappatura.get("separatore", ";")))


def a_decimale(testo, sep_decimale):
    testo = (testo or "").strip().replace("€", "").replace("%", "").strip()
    if not testo:
        return None
    if sep_decimale == ",":
        testo = testo.replace(".", "").replace(",", ".")
    try:
        return Decimal(testo)
    except InvalidOperation:
        return None


def normalizza(riga, mappatura):
    colonne = mappatura["colonne"]
    sep = mappatura.get("separatore_decimale", ",")
    out, avvisi = {}, []
    for campo in CAMPI:
        sorgente = colonne.get(campo, "")
        grezzo = (riga.get(sorgente, "") if sorgente else "").strip()
        if campo in CAMPI_DECIMALI or campo in CAMPI_INTERI:
            valore = a_decimale(grezzo, sep)
            if grezzo and valore is None:
                avvisi.append(f"{campo}: valore non numerico '{grezzo}', lasciato vuoto")
            if valore is not None and campo in CAMPI_INTERI:
                if valore != valore.to_integral_value():
                    avvisi.append(f"{campo}: valore non intero '{grezzo}', lasciato vuoto")
                    valore = None
                else:
                    valore = int(valore)
            out[campo] = "" if valore is None else str(valore)
        else:
            out[campo] = grezzo
    if not out["valuta"] and out["prezzo_acquisto_netto"]:
        out["valuta"] = mappatura.get("valuta_predefinita", "")
    return out, avvisi


def carica_ricarichi(percorso):
    with open(percorso, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter=";") if r.get("ricarico_pct", "").strip()]


def trova_ricarico(regole, cliente, codice, categoria):
    """Priorita': cliente+articolo > articolo > categoria > default."""
    def cerca(livello, **filtri):
        for r in regole:
            if r["livello"] == livello and all(r.get(k, "").strip() == v for k, v in filtri.items()):
                return r
        return None
    candidati = []
    if cliente and codice:
        candidati.append(cerca("cliente_articolo", cliente=cliente, codice_od=codice))
    if codice:
        candidati.append(cerca("articolo", codice_od=codice))
    if categoria:
        candidati.append(cerca("categoria", categoria=categoria))
    candidati.append(cerca("default"))
    return next((c for c in candidati if c), None)


def applica_ricarico(articolo, regole, cliente):
    regola = trova_ricarico(regole, cliente, articolo["codice_od"], articolo["categoria"])
    articolo["ricarico_pct"] = ""
    articolo["regola_ricarico"] = ""
    articolo["prezzo_vendita_netto"] = ""
    if not articolo["prezzo_acquisto_netto"] or regola is None:
        return
    pct = Decimal(regola["ricarico_pct"].replace(",", "."))
    netto = Decimal(articolo["prezzo_acquisto_netto"])
    vendita = (netto * (1 + pct / 100)).quantize(Decimal("0.01"), ROUND_HALF_UP)
    articolo["ricarico_pct"] = str(pct)
    articolo["regola_ricarico"] = regola["livello"]
    articolo["prezzo_vendita_netto"] = str(vendita)


def stampa_confronto(originali, normalizzati, mappatura):
    colonne = mappatura["colonne"]
    for orig, norm in zip(originali, normalizzati):
        print("=" * 78)
        print(f"Articolo {norm['codice_od'] or '(codice mancante)'}")
        print(f"{'campo':26} {'portale/file':24} {'normalizzato':24} esito")
        for campo in CAMPI:
            sorgente = colonne.get(campo, "")
            v_orig = (orig.get(sorgente, "") if sorgente else "").strip()
            v_norm = norm[campo]
            if not sorgente and v_norm:
                esito = "DA CONFIG (non dal file)"
            elif not sorgente:
                esito = "NON MAPPATO"
            elif v_orig == v_norm:
                esito = "uguale"
            elif not v_norm and v_orig:
                esito = "DIFFERENZA: perso"
            elif campo in CAMPI_DECIMALI | CAMPI_INTERI and a_decimale(v_orig, mappatura.get("separatore_decimale", ",")) == Decimal(v_norm or "0"):
                esito = "solo formato"
            else:
                esito = "DIFFERENZA"
            print(f"{campo:26} {v_orig[:24]:24} {v_norm[:24]:24} {esito}")
        print(f"{'prezzo_vendita_netto':26} {'':24} {norm['prezzo_vendita_netto']:24} "
              f"regola={norm['regola_ricarico'] or 'nessuna'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", type=Path, help="esportazione ufficiale in dati/originali/")
    p.add_argument("--cliente", default="", help="codice cliente TASSIUFFICIO per i ricarichi dedicati")
    p.add_argument("--mappatura", type=Path, default=RADICE / "config/mappatura_colonne.json")
    p.add_argument("--ricarichi", type=Path, default=RADICE / "config/ricarichi.csv")
    p.add_argument("--uscita", type=Path, default=RADICE / "dati/campione_normalizzato")
    p.add_argument("--max", type=int, default=10, help="massimo articoli da elaborare (campione)")
    p.add_argument("--confronto", action="store_true", help="mostra file originale accanto al normalizzato")
    a = p.parse_args()

    mappatura = carica_mappatura(a.mappatura)
    if not any(mappatura["colonne"].values()):
        sys.exit("La mappatura colonne e' vuota: compila config/mappatura_colonne.json guardando il file reale.")
    originali = leggi_righe(a.file, mappatura)[: a.max]
    regole = carica_ricarichi(a.ricarichi)

    normalizzati = []
    for i, riga in enumerate(originali, 1):
        art, avvisi = normalizza(riga, mappatura)
        applica_ricarico(art, regole, a.cliente)
        normalizzati.append(art)
        for av in avvisi:
            print(f"[riga {i}] {av}", file=sys.stderr)

    campi_out = CAMPI + ["ricarico_pct", "regola_ricarico", "prezzo_vendita_netto"]
    with open(a.uscita.with_suffix(".csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campi_out, delimiter=";")
        w.writeheader()
        w.writerows(normalizzati)
    with open(a.uscita.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(normalizzati, f, ensure_ascii=False, indent=2)
    print(f"{len(normalizzati)} articoli -> {a.uscita}.csv / .json")

    if a.confronto:
        stampa_confronto(originali, normalizzati, mappatura)


if __name__ == "__main__":
    main()
