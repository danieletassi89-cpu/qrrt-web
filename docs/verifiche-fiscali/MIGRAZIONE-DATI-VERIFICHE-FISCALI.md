# Strategia di migrazione dati — Verifiche fiscali

> **Nessuna importazione eseguita.** Documento di strategia.

## 1. Fonti disponibili

| # | Fonte | Contenuto | Formato | Accessibilità | Stato |
|---|---|---|---|---|---|
| A | **Database vecchio programma** (`dbvf.mdb` + `Db\Azienda.mdb` del tuo PC) | Clienti, MF, marchi/modelli, verifiche, tecnici, laboratorio | Access Jet 4 (`.mdb`, forse `.accdb`) | ✅ Leggibile senza Windows (`mdbtools` già provato sugli schemi) | Servono i **file reali** (quelli installati qui sono vuoti) |
| B | **File trimestrali inviati all'AdE** (se conservati) | Tecnici, clienti, MF, verifiche del trimestre | `.txt` tracciato fisso (record `0MIS0026`…`9MIS0026`) | ✅ Il vecchio programma stesso li reimporta: formato strutturato | Da verificare se li hai |
| C | **FiscalWeb21** | Clienti, punti vendita, RT, verifiche, scadenze, PDF | ⚪ Excel/CSV? PDF? API? | ⚪ Da scoprire nella navigazione | **Fonte principale per gli RT** |
| D | **TASSIUFFICIO Helpdesk** | Clienti (destinazione e chiave di deduplica) | DB Helpdesk | ⚪ serve accesso allo schema | — |
| E | Documenti PDF storici (verbali FiscalWeb21, scansioni) | Prova documentale | PDF | ⚪ | Opzionale |

**Priorità:** C (dati RT attuali e scadenze vive) → A (storico MF e clienti storici) → B (solo se A non è disponibile o incompleto).

## 2. Cosa importare (e cosa no)

| Dato | Importare | Note |
|---|---|---|
| Clienti | **Collegare**, non duplicare | Match su clienti Helpdesk esistenti |
| Punti vendita | Sì | Da FW21; dal vecchio: ricavati da `ecr.ub_*` |
| RT (matricole, modelli, stato, date) | **Sì** | Fondamentale |
| Prossime scadenze | **Sì, ma ricalcolate** | Confronto tra scadenza importata e scadenza ricalcolata; le differenze vanno in revisione |
| Verifiche storiche RT | Sì | Come `CONCLUSA`, `source='IMPORT'`, snapshot, immutabili |
| PDF storici | Sì se esportabili | Allegati come `IMPORTATO` con hash |
| MF storici (vecchio programma) | Sì, solo storico | Stato `DISMESSO` se defiscalizzati, nessuna scadenza attiva salvo tua indicazione |
| Tecnici | Profili fiscali | Collegati a utenti Helpdesk esistenti o creati disattivi |
| Password tecnici (`pw_web`) | **No** | In chiaro nel vecchio DB, non si migrano |
| Fatture Magis | No | Solo `billing_status` sulla verifica |

## 3. Processo di import (per ogni fonte)

```
1. ACQUISIZIONE   copia del file sorgente (mai l'originale), hash SHA-256, registrazione in import_batches
2. ESTRAZIONE     lettura in tabelle di appoggio (import_rows.raw), nessuna scrittura sui dati veri
3. NORMALIZZAZIONE  maiuscole/spazi, P.IVA 11 cifre, CF 16, CAP 5, provincia 2, date, matricola senza spazi
4. MATCHING       proposta azione per ogni riga: CREA / COLLEGA / AGGIORNA / SCARTA / DA_VERIFICARE
5. REPORT         anteprima con conteggi e lista conflitti → revisione tua
6. CONFERMA       scrittura in una transazione per lotto, audit "IMPORT", legacy_ref valorizzato
7. VERIFICA       controlli di integrità post‑import (§6) e campione manuale
8. ANNULLAMENTO   possibile per l'intero batch finché non ci sono verifiche nuove collegate
```

Prove sempre prima su una **copia del database Helpdesk** (ambiente di prova), poi in produzione dopo un **backup**.

## 4. Regole di matching e deduplica

### Clienti
1. **P.IVA** uguale (normalizzata) → COLLEGA.
2. Senza P.IVA: **codice fiscale** uguale → COLLEGA.
3. Nome simile (distanza testuale) + stesso comune → DA_VERIFICARE.
4. Nessuna corrispondenza → CREA (con flag "importato, da controllare").
5. Stessa P.IVA con più clienti Helpdesk → DA_VERIFICARE (non si sceglie in automatico).

### Punti vendita
Cliente + indirizzo normalizzato + CAP → stessa sede. Più RT allo stesso indirizzo condividono la sede.

### Apparecchi
- RT: **matricola** univoca. Stessa matricola in due fonti → unione (FW21 prevale per dati attuali, vecchio per storico).
- MF: **logotipo + matricola**. Il vecchio programma consentiva lo stesso MF su clienti diversi nel tempo → diventa **un apparecchio con storico installazioni**.

### Verifiche
Chiave: apparecchio + data verifica + tipo. Duplicato tra fonti → si tiene quella con più dati (e il PDF), l'altra va in `SCARTA` con motivo.

### Tecnici
**Codice fiscale** (come fa il vecchio programma).

## 5. Mapping di dettaglio

### 5.1 Vecchio programma (fonte A)

| Sorgente | Destinazione | Trasformazione |
|---|---|---|
| `clforn.rag_soc, piva, cf/codfis, indirizzo, cap, citta, prov, tel1, tel2, email, note, nome, cognome` | cliente Helpdesk + contatto | match §4 |
| `ecr.ub_indirizzo, ub_cap, ub_comune, ub_prov` | sede | dedup per cliente+indirizzo |
| `marchio.marchio`, `modello.modello` | `device_manufacturers`, `device_models (category='MF')` | dedup case‑insensitive |
| `ecr.logotipo + matricola` | `fiscal_rt_devices.fiscal_serial`, `device_kind='MF'` | concatenazione senza spazi |
| `ecr.data_inst` | `activated_on` | |
| `ecr.data_defisc` | `decommissioned_on`, `status='DISMESSO'` | se valorizzata |
| `ecr.sospeso` | `status='FUORI_SERVIZIO'` | |
| `ecr.data_ultverifica`, `data_scad_assisenza` | `last_check_date`, `next_due_date` (solo se RT attivo, ⚪) | vedi domanda 5 dell'analisi |
| `ecr.tipo`, `prezzo`, `scad_gar`, `nota_ecr` | `contract_type`, `default_price`, `warranty_until`, note | |
| `visure.*` | `fiscal_checks` | `tipoint`→`check_type`, `esito`→`outcome`, `data_initv`→`started_at`, `data_finev`→`completed_at`, dati copiati → `snapshot` |
| `visure.idtecnico/cftecnico` | `technician_profile_id` | match per CF |
| `visure.importo, pagato, fatturato, idfatt` | `amount, is_paid, billing_status, billing_ref` | |
| `tecnico_incaricato` | `fiscal_technician_profiles` | niente `pw_web` |
| `soggetto_obbligato` | `fiscal_lab_settings` | solo se vuoto |

Strumento: `mdb-export` (mdbtools) → CSV → import. Nessun Windows/Access necessario.

### 5.2 File trimestrali AdE (fonte B)
- Il tracciato (specifiche AdE 2010) va ricostruito dal documento ufficiale o dedotto da un file reale. Il vecchio programma ne estrae **tecnici, clienti, MF e verifiche**, quindi il contenuto è sufficiente per ricostruire lo storico degli ultimi trimestri.
- ⚪ Servirà almeno un file di esempio.

### 5.3 FiscalWeb21 (fonte C) — da definire dopo la navigazione
Da scoprire:
1. Esiste un **export completo** (non solo elenchi a video)? Per quali entità?
2. Formato: Excel/CSV (preferibile), PDF (solo come documento), API?
3. Contiene **identificativi stabili** (codice cliente, id RT) per importazioni ripetute?
4. I **verbali PDF** sono scaricabili in blocco?
5. Le scadenze sono esportate o solo calcolate a video?

Se non esiste un export completo: piano B = export degli **elenchi filtrati** (clienti, RT, verifiche) sezione per sezione + PDF scaricati; piano C = inserimento assistito da elenco stampato (ultima scelta).

## 6. Controlli di integrità

Prima della conferma:
- Conteggi per entità: letti / creati / collegati / scartati / da verificare (devono tornare).
- Matricole duplicate, formati non validi.
- RT attivi **senza scadenza** o con scadenza nel passato remoto.
- Verifiche senza apparecchio o senza tecnico.
- Clienti senza P.IVA/CF.
- Scadenza importata ≠ scadenza ricalcolata (lista differenze).

Dopo la conferma:
- Somma verifiche per anno uguale alla fonte.
- 10 RT a campione controllati da te contro FiscalWeb21 (dati, ultima verifica, scadenza, PDF).
- Dashboard: numero di scadute/in scadenza confrontato con FiscalWeb21 alla stessa data.

## 7. Transizione

1. Periodo di **doppio lavoro limitato** (es. 2–4 settimane): FiscalWeb21 resta la fonte ufficiale, il modulo in prova.
2. **Import delta** finale (solo le verifiche fatte nel frattempo) poco prima del passaggio.
3. Data di passaggio: da quel giorno le verifiche nascono solo nell'Helpdesk.
4. Conservare **export completo e PDF** di FiscalWeb21 archiviati (valore documentale) prima di un'eventuale disdetta.

## 8. Cosa serve da te

- [ ] Copia di `dbvf.mdb` e `Db\Azienda.mdb` reali (o conferma che non esistono più).
- [ ] Eventuali file trimestrali `.txt`.
- [ ] Navigazione di FiscalWeb21 nella sezione export.
- [ ] Accesso (in lettura) allo schema del database Helpdesk o a un suo export clienti.
