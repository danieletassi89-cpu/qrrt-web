# Verifica integrazione OD+ → portale TASSIUFFICIO

Stato al 30/09/2026. **Bozza preliminare: nessuna verifica sul portale OD+ è ancora stata eseguita.**

## 1. Verifiche realmente eseguite

| # | Verifica | Esito | Evidenza |
|---|----------|-------|----------|
| 1 | Lettura pagine pubbliche `www.odplus.it/servizi/web/edi/` e `/configuratore-edi/` | **Non eseguita** | L'ambiente cloud usato ha rifiutato la connessione (proxy 403 verso odplus.it). La richiesta non ha raggiunto OD+. |
| 2 | Lettura della pagina di login `b2b.odplus.it` | **Non eseguita** | Stesso blocco di rete. |
| 3 | Condizioni d'uso (automazione, riuso su siti terzi) | **Non eseguita** | Da fare come primo passo nella sessione locale. |
| 4 | Area riservata, esportazioni, rete, campi | **Non eseguita** | Serve il login fatto a mano dal titolare nella sessione locale con browser visibile. |
| 5 | Prototipo di importazione | **Provato solo su dati sintetici** | `importatore/importa.py` testato su un CSV di prova inventato (non OD+), fuori dal progetto: parsing numeri IT, campi mancanti lasciati vuoti, priorità dei ricarichi. |

## 2. Condizioni d'uso OD+

**Da verificare.** Sezione da compilare citando testualmente le clausole su:
- uso automatizzato (script, robot, estrazione dati);
- riuso di catalogo, immagini e prezzi su siti di terzi;
- riservatezza dei prezzi riservati.

Se vietano l'automazione, ci si ferma e si decide con il titolare.

## 3. Metodi disponibili × campi recuperabili

Legenda: ✅ verificato · ❌ assente · ? da verificare · — non applicabile

| Campo | Export ufficiale (CSV/Excel) | Pagine portale (HTML) | Richieste viste nel browser* | EDI Anagrafica | EDI Documenti |
|---|---|---|---|---|---|
| codice_od | ? | ? | ? | ? | ? |
| ean | ? | ? | ? | ? | ? |
| cod_produttore | ? | ? | ? | ? | ? |
| nome / descrizione | ? | ? | ? | ? | — |
| marca / categoria | ? | ? | ? | ? | — |
| immagine_url | ? | ? | ? | ? | — |
| prezzo netto riservato | ? | ? | ? | ? | ? |
| valuta / IVA escl.-incl. | ? | ? | ? | ? | ? |
| unità vendita / pz per conf. / qta minima | ? | ? | ? | ? | — |
| giacenza (quantità o generica) | ? | ? | ? | ? | — |
| tempi di approvvigionamento | ? | ? | ? | ? | — |
| data aggiornamento | ? | ? | ? | ? | ? |

\* Un'API vista nel browser **non** è un'API ufficiale né autorizzata.

### Possibilità tecnica, autorizzazione, affidabilità

| Metodo | Tecnica | Autorizzazione uso commerciale | Affidabilità nel tempo |
|---|---|---|---|
| Export ufficiale | ? | ? (dipende dalle condizioni) | Media: il formato può cambiare |
| Lettura pagine HTML | ? | Probabilmente da chiedere | Bassa: cambia con la grafica |
| Richieste di rete del browser | ? | **Non autorizzata** salvo accordo scritto | Bassa: non documentate |
| EDI Anagrafica | Pubblicizzata, non provata | Contrattuale (a pagamento) | Alta |

## 4. Costi

| Voce | Costo | Fonte |
|---|---|---|
| EDI Ordini | Gratuito | Pubblicizzato su odplus.it (riferito dal titolare, non riletto da me) |
| EDI Documenti | da 9 €/mese | Pubblicizzato su odplus.it (riferito dal titolare, non riletto da me) |
| EDI Anagrafica | **Non pubblicato** | Da chiedere |

**Da chiedere a OD+:**
1. Canone e costi di attivazione di EDI Anagrafica, frequenza di aggiornamento, formato (CSV/XML/EDIFACT), campi inclusi (giacenze? immagini?).
2. Se prezzi netti riservati e giacenze sono inclusi nell'anagrafica o in un flusso separato.
3. Licenza d'uso di immagini e descrizioni su un portale di vendita TASSIUFFICIO.
4. Requisiti tecnici e costi di EDI Ordini (formato, canale, test).
5. Se è consentita l'esportazione periodica dal portale B2B per uso interno o commerciale.
6. Se l'accesso EDI è già incluso nel contratto attuale (non va presunto).

## 5. Prototipo

- `importatore/importa.py`: normalizza l'esportazione, applica i ricarichi, scrive `dati/campione_normalizzato.csv` e `.json`; `--confronto` mostra valori del file accanto a quelli normalizzati.
- `config/mappatura_colonne.json`: da compilare sulle colonne reali del file OD+.
- `config/ricarichi.csv`: regole con priorità cliente+articolo > articolo > categoria > default.
- Il prezzo di vendita è calcolato sul netto, IVA esclusa, **per la stessa unità del prezzo d'acquisto** (nessuna conversione pezzo/confezione).

## 6. Flusso ordini (valutazione, nulla eseguito)

1. **Fase 1, inoltro manuale:** il cliente ordina sul portale TASSIUFFICIO. L'ordine viene salvato ed esportato (CSV/PDF con codice_od e quantità nell'unità di vendita OD+). Un operatore lo reinserisce sul B2B OD+, eventualmente con una funzione di importazione carrello da file, se esiste (da verificare). È l'opzione più semplice e senza vincoli.
2. **Fase 2, EDI Ordini (gratuito secondo OD+):** l'ordine d'acquisto verso OD+ viene generato nel formato EDI richiesto. Prima servono specifiche, ambiente di test e conferma contrattuale.
3. Controlli necessari in entrambi i casi: rispetto di quantità minime e multipli di confezione, verifica di prezzo e disponibilità al momento dell'ordine, gestione di conferme e evasioni parziali (EDI Documenti).

## 7. Conclusione

**Non ancora dimostrato.** L'integrazione non è stata provata: nessun dato OD+ è stato letto e le condizioni d'uso non sono state verificate. Il prototipo funziona solo su dati sintetici.

## 8. Percorso più semplice per la prima versione

1. Chiedere a OD+ le condizioni d'uso e il costo di EDI Anagrafica (vedi §4).
2. Nel frattempo, se consentito, esportare manualmente un listino ufficiale filtrato sui prodotti venduti da TASSIUFFICIO.
3. Importarlo con il prototipo, applicare i ricarichi e pubblicare il catalogo sul portale.
4. Raccogliere gli ordini sul portale e inoltrarli a mano su OD+.
5. Passare a EDI Anagrafica ed EDI Ordini quando volumi e costi lo giustificano.
