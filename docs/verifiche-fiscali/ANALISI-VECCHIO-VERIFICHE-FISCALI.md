# Analisi del vecchio software "VerificheFiscali" (Windows)

> Fase: **analisi** — nessuna modifica a TASSIUFFICIO Helpdesk, nessun database toccato.
> Data analisi: 30/09/2026.

## Legenda affidabilità

| Simbolo | Significato |
|---|---|
| ✅ **VERIFICATO** | Letto direttamente dai file (schema database, definizioni dei form, modelli di stampa, stringhe dell'eseguibile). |
| 🟡 **DEDOTTO** | Ricavato con buona certezza dal codice (query SQL, nomi di eventi, testi dei messaggi), ma non osservato a programma in esecuzione. |
| ⚪ **IPOTESI** | Interpretazione plausibile, da confermare con te o con i tuoi dati reali. |

---

## 1. Cosa è stato fornito e cosa ne è stato fatto

### 1.1 Il file `VerificheFiscali.exe` è il setup, non il programma ✅

| Proprietà | Valore |
|---|---|
| Dimensione | 12.810.483 byte |
| SHA-256 | `95ab4db1a5482be3c900b927aef8ccaed3614acc70f9f01b76fffd5616171f42` |
| Tipo | PE32 (Windows 32 bit), **installer "CreateInstall Free" (motore Gentee)** |
| Metadati | `ProductName: VerificheFiscali 1.1` — `FileVersion: 1.1.13` — `CompanyName: Magis Software` — `© 2017 Magis Software` |
| Contenuto | archivio compresso (overlay di ~12,7 MB, entropia 8 bit/byte, compressione proprietaria Gentee) |

### 1.2 Procedura seguita (non distruttiva)

1. Il file originale **non è stato modificato**: ne è stata fatta una copia nella cartella temporanea di lavoro.
2. La copia è stata installata in una **sandbox Wine isolata** (un "finto Windows" usa‑e‑getta), accettando la procedura guidata standard. Nessun effetto sul tuo PC o sui tuoi dati.
3. I file installati sono stati analizzati **staticamente**:
   - schemi dei database Access (`mdbtools`);
   - definizioni dei form Delphi (risorse `RCDATA/TPF0` decodificate: 430 form);
   - modelli di stampa FastReport (`.fr3` XML, `.frf`);
   - stringhe e query SQL contenute nell'eseguibile.
4. **Avvio del programma**: tentato, ma in sandbox va in errore all'avvio perché manca il motore Microsoft Jet/DAO (il download da Microsoft è bloccato dalla rete della sandbox). Le schermate sono quindi **ricostruite dalle definizioni dei form**, che contengono titoli, menu, etichette, campi collegati al database, colonne delle griglie e voci delle tendine. ⚠️ Non ho screenshot reali del programma in funzione: se vuoi, puoi mandarmene qualcuno dal tuo PC.

### 1.3 Contenuto dell'installazione ✅

Cartella di installazione predefinita: `C:\Programmi\Magis Software\VerificheFiscali\`

| File | Dimensione | Ruolo |
|---|---|---|
| `VerificheFiscali.exe` | 19,1 MB (17/10/2017) | **Programma principale** (Delphi, Borland VCL). È un eseguibile "multi‑prodotto" Magis: contiene anche moduli di cassa, magazzino, fatturazione, e‑commerce, ottica… di cui qui viene usata solo la parte verifiche fiscali. |
| `Assistenza.exe` | 6,1 MB (20/10/2016) | Modulo **GestLab** — schede di riparazione/laboratorio (collegamento "Menu Start › GestLab"). |
| `Promo.exe` | 1,2 MB | Promozioni/volantini: non pertinente. |
| `dbvf.mdb` | 372 KB | **Database delle verifiche fiscali** (Access/Jet 4). |
| `Db\Azienda.mdb` | 1,9 MB | Database gestionale Magis condiviso: **clienti** (`clforn`), fatture, dati azienda, utenti… |
| `Db\laboratorio.mdb` | 413 KB | Database delle schede di riparazione (GestLab). |
| `contatti.mdb` | 905 KB | Tabella `comuni` (8.304 comuni con provincia, regione, CAP, codice catastale). |
| `*.fr3`, `PReports\*.frf` | — | Modelli di stampa FastReport (vedi §6). |
| `ico\*.bmp` | — | Icone raster 24×24 della toolbar. |
| `uninstall.exe/.ini` | — | Disinstallazione. |

> ⚠️ **I database installati sono vuoti** (è un'installazione nuova). I tuoi dati reali sono nei file `dbvf.mdb` e `Db\Azienda.mdb` **del PC dove usavi il programma**. Per la migrazione servono quei file (vedi `MIGRAZIONE-DATI-VERIFICHE-FISCALI.md`).

---

## 2. Natura del programma

| Aspetto | Esito |
|---|---|
| Ambito | ✅ Gestione delle verifiche su **Misuratori Fiscali (MF)**, cioè i registratori di cassa **pre‑RT** con logotipo + matricola, giornale di fondo elettronico (DGFE) e libretto fiscale cartaceo. |
| Periodicità gestita | ✅ Testo del programma: *"gestire l'attività di verificazione **annuale** su Misuratori Fiscali"*. |
| Normativa citata | ✅ Direttiva/provvedimento Agenzia Entrate **n. 13635 del 29/03/2010** (specifiche del file trimestrale). In un altro testo è scritto "10635/2010": refuso del programma. |
| Registratori Telematici (RT) | ❌ **Non gestiti**. Il programma è del 2017, antecedente all'obbligo RT. Campi e logiche (logotipo 2 caratteri, matricola 9, azzeramenti, DGFE, file trimestrale) sono tipici degli MF. |
| Architettura | ✅ Desktop monoutente, database Access locale, connessione DAO (`TKADaoDatabase`), stampe FastReport, esportazione PDF/RTF/JPEG/XLSX. |
| App mobile | ✅ Esisteva un'**app Android** "Verifiche Fiscali" per i tecnici, sincronizzata tramite **FTP** con un server Magis (vedi §5.9). |
| Licenza | ✅ Attivazione online (codice installazione/attivazione, verifica su server Magis), versione DEMO limitata nell'export. |

**Conseguenza per il progetto:** il vecchio programma è un ottimo riferimento per **struttura dati, rapidità e documenti**, ma il suo modello "MF" va aggiornato al mondo RT (matricola a 11 caratteri, verificazione **biennale**, esito registrato sul portale AdE "Fatture e Corrispettivi", QR code del dispositivo, niente DGFE né file trimestrale).

---

## 3. Struttura dell'applicazione (menu e schermate)

### 3.1 Finestra principale "Gestione Verifiche Fiscali" ✅ (`Tfmaingvf`)

**Barra pulsanti grandi** (in ordine):

1. Nuovo Cliente
2. Gestione Clienti
3. Aggiungi Nuovo Misuratore Fiscale
4. Nuova Verificazione Fiscale
5. Gestione Misuratori Fiscali
6. Gestione Verifiche Fiscali
7. **Crea File Trimestrale per Agenzia delle Entrate**
8. Crea Scheda Riparazione

**Menu principale:**

```
Impostazioni
 ├─ Soggetto Obbligato...
 ├─ Tecnici Incaricati...
 ├─ Marchi Produttori...
 ├─ Modelli Misuratori Fiscali...
 └─ Stampe...                 (editor dei modelli di stampa FastReport)
Archivio
 ├─ Clienti            › Gestione... / Nuovo Cliente...
 ├─ Misuratori Fiscali › Gestione... / Nuovo Misuratore Fiscale...
 ├─ Verifiche Periodiche › Gestione... / Nuova Verifica Fiscale...
 └─ Schede Riparazione › Crea Scheda Riparazione...
Utility
 ├─ Controlla Aggiornamenti Software...
 ├─ Attiva Licenza d'uso...
 ├─ Importa Dati da Precedenti File di Invio...
 └─ Sincronizza Dati con il Server...
```

**Corpo della finestra = scadenziario** (è la "dashboard" del vecchio programma):

- **Calendario** (`TPlannerCalendar`) che evidenzia le *"Giornate con Misuratori Fiscali con Verifica in scadenza"*; trascinando col mouse si seleziona un periodo.
- Pannello **"Scadenziario Verifiche M.F."** con filtri: **Località**, **Prov.**, **Ragione sociale cliente**, pulsante *Nessuna selezione*, pulsante *Stampa*.
- Griglia con colonne: `Cod. | Scad. Assistenza | Ult. Verifica | Marchio | Modello | Logotipo | Matricola | Tipo | Nominativo o Ragione Sociale | Località | Prov. | Prezzo`.
- **Menu tasto destro** sulla griglia: Modifica dati cliente · Modifica dati misuratore · **Inserisci verifica fiscale** · Stampa elenco · **Stampa tagliandi** · Stampa lista di controllo (verifica periodica) · Stampa lista di controllo (prima installazione).

🟡 Query dello scadenziario:
```sql
SELECT ecr.* FROM ecr
WHERE ecr.data_scad_assisenza >= #da# AND ecr.data_scad_assisenza <= #a#
  AND ecr.no_scad = False AND ecr.sospeso = False
ORDER BY ecr.data_scad_assisenza DESC
```
→ lo scadenziario si basa sul campo **`data_scad_assisenza`** (scadenza assistenza/verifica) ed esclude gli apparecchi **sospesi** o marcati **"Non mostrare nello scadenziario"**.

> 💡 Punto di forza da conservare: **dalla schermata iniziale si arriva alla nuova verifica con un clic destro** sulla riga in scadenza.

### 3.2 Elenco Misuratori Fiscali ✅ (`Tele_mf`)

- Pulsanti: Visualizza tutti · Nuovo · Modifica · Elimina · Stampa · **Operazioni sul M.F.** · Crea scheda riparazione · Chiudi.
- **Ricerca** con 9 campi: codice, ragione sociale, indirizzo, località, provincia, logotipo, matricola, marchio, modello (ricerca "contiene", filtri combinati in AND).
- **Filtri rapidi** (caselle):
  - *MF in esaurimento (rimanenti 30 azzeramenti)* → `(n_azzeraenti + 30) > max_azz AND max_azz > 0`
  - *MF in garanzia* → `scad_gar > oggi`
  - *Solo MF attivi* → `data_defisc IS NULL AND sospeso = false`
  - *Solo MF sospesi* → `sospeso = true`
  - *Solo MF defiscalizzati* → `data_defisc IS NOT NULL`
- Griglia: `Cod. | Nominativo | Tipo | Località | Prov. | Logotipo | Matricola | Marchio | Modello | N. Max Azz. | N. Azzer.`
- **Menu "Operazioni sul M.F."**: Installazione ad altro cliente · Rimessa in servizio · Messa in servizio · **Verifica periodica** · Defiscalizzazione.
- 🟡 Regola: *"Impossibile eliminare Misuratore Fiscale per il quale sono state inserite delle verificazioni"* (integrità referenziale applicativa).

### 3.3 Scheda "Misuratore Fiscale" ✅ (`Tfmis_fiscale`)

| Gruppo | Campi |
|---|---|
| **Dati identificativi** | Logotipo · Matricola · Marchio produttore · Modello (pulsante *Scegli marca e modello*) · Ragione sociale cliente (pulsante *Scegli cliente*) · N. azzeramenti · N. max azzeramenti · **Tipo** (*Singolo intervento / Noleggio / Contratto*) · **Ultimo prezzo pagato** · **Sospeso** |
| **Ubicazione esercizio commerciale** | Comune · Prov. · Indirizzo · CAP |
| **Agenda** | Data installazione · Data defiscalizzazione · Data scadenza garanzia · Data ultima verificazione · **Data scadenza assistenza** · *Non mostrare nello scadenziario* |
| Note | Nota sul misuratore · Nota sul cliente (memo del cliente, modificabile da qui) |

> 💡 Osservazione: l'**ubicazione** (punto vendita) è salvata **dentro il misuratore**, non come entità separata: semplice ma duplica gli indirizzi se un cliente ha più casse nello stesso negozio.

### 3.4 Scheda "Dati Verifica Fiscale" ✅ (`Tfverificamf`)

| Gruppo | Campi |
|---|---|
| Dati identificativi MF | Logotipo · Matricola · Marchio · Modello · Cliente · N. azzeramenti · N. max azzeramenti |
| Ubicazione | Comune · Prov. · Indirizzo · CAP |
| **Specifiche verificazione** | Data inizio verifica · Data fine verifica · **Tipo verifica** · **Esito** · **Tecnico incaricato** (pulsante di scelta) |
| Economici | **Importo verifica** · **Pagato** |

Valori delle tendine:
- **Tipo verifica**: `MESSA IN SERVIZIO` · `DEFISCALIZZAZIONE` · `VERIFICA PERIODICA` · `MESSA IN SERVIZIO E VERIFICA PERIODICA`
- **Esito**: `ESITO POSITIVO` · `ESITO NEGATIVO`

> ⚠️ **La verifica è una "fotocopia" dei dati del misuratore** (marchio, modello, cliente, ubicazione copiati nel record `visure`). Vantaggio: lo storico resta fedele anche se il cliente cambia indirizzo. Svantaggio: nessun vincolo reale tra verifica e apparecchio (il legame è solo logotipo+matricola+idcliente).

> ⚠️ **Non c'è una checklist digitale**: gli esiti dei singoli controlli (A1…F2) non vengono registrati. La checklist esiste solo **stampata su carta** e compilata a penna (vedi §6).

### 3.5 Effetti automatici del salvataggio di una verifica 🟡

Ricostruiti dalle istruzioni SQL presenti nell'eseguibile:

| Tipo intervento | Aggiornamento dell'anagrafica misuratore (`ecr`) |
|---|---|
| **VERIFICA PERIODICA** | `data_ultverifica = data verifica`, `data_scad_assisenza = nuova scadenza`, `max_azz = …` |
| **MESSA IN SERVIZIO** | `data_defisc = NULL`, `no_scad = false`, aggiornamento `max_azz`, `n_azzeraenti`, `prezzo` |
| **DEFISCALIZZAZIONE** | `data_defisc = data`, `no_scad = true` (esce dallo scadenziario) |

⚪ **IPOTESI**: la nuova scadenza è calcolata a **+1 anno** (coerente con la verificazione annuale MF dichiarata dal programma). Non ho trovato la costante nel codice compilato; va confermato con i tuoi dati (differenza tra `data_ultverifica` e `data_scad_assisenza`).

### 3.6 Elenco Verifiche Fiscali ✅ (`Tfele_visuremf`)

- Pulsanti: Visualizza tutti · Nuovo · Modifica · Elimina · Stampe · Chiudi.
- **Ricerca**: numero, logotipo, matricola, marchio, modello, cliente, **P.IVA cliente**, tecnico, tipo verifica, **intervallo date** (da/a).
- Griglia: `Num. | Logotipo | Matricola | Data verifica | Tipo verifica | Marchio | Modello | Cliente | Tecnico | Ubicazione | Importo | Fatturato | Pagato` con **conteggio righe a piè di griglia**.
- **Menu stampe/azioni**: Dichiarazione di messa in servizio · Dichiarazione di defiscalizzazione · Lista di controllo verifica periodica · Lista di controllo prima installazione · Stampa elenco · **Crea fattura** · **Stampa fattura**.

> 💡 Punto di forza: **fatturazione diretta dalla verifica** (campi `fatturato`, `idfatt`, `pagato`) usando il modulo fatture del gestionale Magis.

### 3.7 Soggetto Obbligato (il laboratorio) ✅ (`Tfsogg_obbli`)

- Tipologia: *Persona fisica / Persona giuridica*
- **Dati aziendali**: denominazione, comune/provincia/indirizzo/CAP del domicilio fiscale, e‑mail, telefono
- **Dati personali**: cognome, nome, sesso, data/luogo/provincia di nascita
- **Dati identificativi**: codice fiscale, partita IVA, **Tipo abilitazione** (*Fabbricante abilitato / Laboratorio autonomo*), **Identificativo alfabetico del sigillo**
- Opzioni sincronizzazione: *Sincronizza sempre all'apertura*, *Connessione FTP passiva*

### 3.8 Tecnici Incaricati ✅ (`Tftecnico_inc`, `Tele_tecnici_inc`)

- Codice fiscale, titolo di studio (*Nessuno / Elementare / Media inferiore / Media superiore / Laurea*), **Responsabile laboratorio** (SI/NO), cognome, nome, sesso, dati di nascita
- **Data inizio / fine collaborazione**
- **Identificativo alfabetico e numerico del sigillo** (il punzone personale del tecnico)
- **Portale web**: *Abilita accesso del tecnico al portale/app*, password di accesso

### 3.9 Marchi e Modelli ✅

- Elenco **marchi produttori** (solo nome).
- Elenco **modelli** (modello + marchio). Scelta guidata "marca → modello" dalla scheda misuratore.

### 3.10 Anagrafica cliente (versione semplificata "VF") ✅ (`TNEWCLI_VF`)

Ragione sociale/nome ditta · indirizzo · CAP · località · prov. · P.IVA · codice fiscale · telefono · cellulare · e‑mail · note · **persona di riferimento** (nome, cognome).
Salvata nella tabella generale `clforn` del gestionale Magis (`Azienda.mdb`).

### 3.11 Schede riparazione (GestLab, `Assistenza.exe` + `laboratorio.mdb`) ✅

- Accettazione: numero scheda, data, cliente (nominativo, indirizzo, telefono, e‑mail), tipo/marca/modello apparecchio, seriale (IMEI), **in garanzia**, documento d'acquisto (numero/data), **accessori consegnati**, **difetto dichiarato** (con causali standard), acconto.
- Lavorazione: **stato** (*In lavorazione / Riparato / Non riparato / Spedito / Consegnato*, con colore), intervento effettuato, costo, laboratorio esterno (operatore, data invio), archiviazione, allegato scansionato.
- Comunicazione al cliente via **SMS/e‑mail** con modelli di messaggio.
- Stampe: **ricevuta di accettazione** (A4, A5, 80 mm), **consegna**, **etichetta**, **DDT**.
- Dal misuratore fiscale si può aprire direttamente *"Crea scheda riparazione per il MF selezionato"*.

> Nell'Helpdesk queste funzioni corrispondono presumibilmente a **ticket/accettazioni**: non vanno duplicate nel modulo fiscale.

---

## 4. Modello dati (database `dbvf.mdb`) ✅

### 4.1 Tabelle

**`ecr`** — il misuratore fiscale installato (una riga per apparecchio‑cliente)

| Campo | Tipo | Significato |
|---|---|---|
| `id` | Long | Codice interno |
| `idmarchio`, `marchio` | Long, Text(40) | Marchio (id + testo copiato) |
| `idmodello`, `modello` | Long, Text(40) | Modello (id + testo copiato) |
| `logotipo` | Text(2) | Logotipo fiscale |
| `matricola` | Text(9) | Matricola |
| `ub_comune`, `ub_prov`, `ub_indirizzo`, `ub_cap` | Text | **Ubicazione** (punto vendita) |
| `idcliente`, `cliente`, `piva` | Long, Text(60), Text(11) | Cliente (id + copia di nome e P.IVA) |
| `data_inst` | Date | Installazione |
| `data_defisc` | Date | Defiscalizzazione (se valorizzata = dismesso) |
| `data_scad_assisenza` | Date | **Scadenza** (usata dallo scadenziario) |
| `data_ultverifica` | Date | Ultima verificazione |
| `scad_gar` | Date | Scadenza garanzia |
| `no_scad` | Bool | Escludi dallo scadenziario |
| `sospeso` | Bool | Apparecchio sospeso |
| `max_azz`, `n_azzeraenti` | Long | Capacità memoria fiscale / azzeramenti effettuati |
| `tipo` | Text(24) | Singolo intervento / Noleggio / Contratto |
| `prezzo` | Double | Ultimo prezzo pagato |
| `nota_ecr` | Text(255) | Nota |

**`visure`** — le verificazioni (una riga per intervento). Contiene **tutti i campi di `ecr`** (copia) più:

| Campo | Significato |
|---|---|
| `data_initv`, `data_finev` | Inizio / fine verifica |
| `tipoint` | Tipo intervento (4 valori, §3.4) |
| `esito` | Esito (positivo/negativo) |
| `idtecnico`, `tecnico`, `cftecnico` | Tecnico (id + copia nome e codice fiscale) |
| `importo` | Importo addebitato |
| `web` | Verifica arrivata dall'app mobile ⚪ |
| `fatturato`, `idfatt`, `pagato` | Stato amministrativo |

**`soggetto_obbligato`** — dati del laboratorio (§3.7).
**`tecnico_incaricato`** — tecnici (§3.8), inclusi `id_alfa`/`idnum` sigillo, `abilita_web`, `pw_web` (**password in chiaro**).
**`marchio`** (`id`, `marchio`) e **`modello`** (`id`, `modello`, `marchio`, `idmarchio`).

### 4.2 Relazioni (logiche, non dichiarate nel DB) 🟡

```
clforn (Azienda.mdb) 1 ──< ecr >── 1 modello >── 1 marchio
                              │
                              └── (logotipo + matricola + idcliente) 1 ──< visure >── 1 tecnico_incaricato
soggetto_obbligato: riga unica (il laboratorio)
```

- Nessuna chiave esterna reale: i legami sono applicativi.
- Molti dati sono **copiati** (denormalizzati): nome cliente, P.IVA, marchio, modello, tecnico.
- 🟡 Evoluzione dello schema tramite `ALTER TABLE` all'avvio (campi aggiunti nel tempo: `scad_gar`, `sospeso`, `nota_ecr`, `tipo`, `prezzo`, `importo`, `web`, `pagato`, `fatturato`, `idfatt`, `max_azz`, `n_azzeraenti`, `abilita_web`, `pw_web`, `auto_sincro`, `ftp_passiva`) e una query di riallineamento della P.IVA da `ecr` a `visure`.
- 🟡 Il programma cerca anche un `dbvf.accdb` (formato Access più recente): possibile che nelle versioni successive il DB sia `.accdb`.

### 4.3 Tabella clienti `clforn` (in `Azienda.mdb`) ✅ — campi rilevanti

`codice`, `rag_soc`, `indirizzo`, `cap`, `citta`, `prov`, `tel1`, `tel2`, `fax`, `piva`, `cf`/`codfis`, `email`, `note`, `cognome`, `nome`, `web`, `clnt`/`forn` (cliente/fornitore), `codditta`, `coddispositivo`, `codpa` (codice destinatario SDI) e decine di campi del gestionale (listini, fidelity, agenti…) non pertinenti.

---

## 5. Funzioni del programma (input → elaborazione → output)

| # | Funzione | Input | Elaborazione | Output |
|---|---|---|---|---|
| 5.1 | Nuovo cliente | Dati anagrafici | Inserimento in `clforn` | Cliente disponibile |
| 5.2 | Nuovo misuratore | Marca/modello, logotipo, matricola, cliente, ubicazione, date, tipo contratto | Copia dati cliente, inserimento `ecr` | MF nello scadenziario |
| 5.3 | Scadenziario | Periodo (calendario), filtri località/prov./cliente | Query su `data_scad_assisenza`, esclusi sospesi/no_scad | Elenco da verificare + stampa |
| 5.4 | Nuova verifica | MF (da scadenziario o elenco), date, tipo, esito, tecnico, importo | Inserimento `visure` + aggiornamento `ecr` (§3.5) | Nuova scadenza, storico |
| 5.5 | Operazioni sul MF | Scelta operazione | Messa in servizio / verifica / defiscalizzazione / rimessa in servizio / **installazione ad altro cliente** (cambio proprietario) | Stato MF aggiornato |
| 5.6 | Stampe verifica | Verifica selezionata | FastReport | Dichiarazioni, checklist, elenco (PDF/stampa) |
| 5.7 | Fatturazione | Verifica | Crea fattura nel gestionale Magis | `fatturato=true`, `idfatt` |
| 5.8 | **File trimestrale AdE** | Anno, trimestre, soggetto obbligato | Selezione verifiche del trimestre, controlli (tecnico con sigillo, P.IVA cliente presenti), tracciato a record fissi `0MIS0026 … 9MIS0026` | File `.txt` da inviare con Entratel |
| 5.9 | **Sincronizzazione app** | Tecnici abilitati | Upload su server Magis del calendario verifiche, download verifiche fatte dai tecnici via app Android | Verifiche importate (flag `web`) |
| 5.10 | **Importa da file di invio** | Ultimi 4 file trimestrali `.txt` | Parsing tracciato AdE, creazione tecnici, clienti, MF, verifiche (dedup per CF tecnico, P.IVA cliente, logotipo+matricola) | Archivio ricostruito |
| 5.11 | Schede riparazione | Da MF o da GestLab | Accettazione → lavorazione → consegna | Ricevute, DDT, etichette |

### 5.8 Dettaglio del file trimestrale 🟡
- Testo del programma: *"file dei dati tecnici relativi alle verifiche sui misuratori fiscali per il trimestre selezionato secondo le specifiche tecniche stabilite dalla direttiva Agenzia delle Entrate N. 13635 del 29/03/2010"*.
- Record di testa `0MIS0026`, record di coda `9MIS0026`, date in formato `ddmmyyyy`, campi a lunghezza fissa riempiti con spazi/zeri.
- Controlli bloccanti: *"Verifica Fiscale per il M.F. matricola … senza riferimento Tecnico Incaricato"*, *"Per il Cliente … non è stata inserita Partita Iva"*.
- Tipi esportati: VERIFICA PERIODICA, MESSA IN SERVIZIO, DEFISCALIZZAZIONE, con esito.

> ⚪ Per gli **RT** questo adempimento **non esiste più** in questa forma: l'esito della verificazione è registrato dal tecnico tramite i servizi AdE (portale "Fatture e Corrispettivi"/procedure di gestione dispositivi) e il libretto diventa elettronico. **Da confermare con te** come lavori oggi (tramite FiscalWeb21? direttamente sul portale AdE?).

> 💡 **Opportunità di migrazione**: se possiedi ancora i **file trimestrali `.txt`** inviati negli anni, sono una fonte dati strutturata e standard (vedi documento migrazione).

---

## 6. Documenti e stampe prodotti ✅

| Modello | Contenuto | Dati |
|---|---|---|
| `check_verifica.fr3` / `controllo_verifica.fr3` | **"Lista di controllo per la verificazione periodica di MF con sigillo integro"** (immagine A4 del modulo + dati sovrapposti) | Laboratorio (denominazione, indirizzo, P.IVA), cliente e ubicazione, marchio, modello, logotipo+matricola |
| `check_prima.fr3` / `controllo_prima.fr3` | **"Lista di controllo… – Prima installazione"** | idem |
| `dic_messa_serv.fr3` | **Dichiarazione di messa in servizio di MF** | Titolare, ditta, sede, matricola, marca, modello, tecnico e CF, "sigillo per conto del…", luogo/data, firme *L'Utente* / *Il Tecnico* |
| `dic_defiscalizza.fr3` | **Dichiarazione di defiscalizzazione di MF** | idem |
| `ele_mf.fr3` / `elencocli_mf.fr3` | Elenco misuratori (con azzeramenti rimanenti, scadenza, tipo, prezzo) | Intestazione laboratorio con tipo abilitazione e **sigillo** |
| `ele_visure_mf.fr3` | Elenco verifiche (data, tipo, esito) | idem |
| `tagliandi.fr3` | **Tagliandi**: etichette/cartellini per apparecchio con ultima verifica, scadenza, azzeramenti | ⚪ probabilmente promemoria da applicare sull'apparecchio o da consegnare |
| `stampafattura.fr3`, `stampaddt.fr3` | Fattura, DDT | — |
| `ricevuta_laboratorio*.fr3`, `consegna_laboratorio*.fr3`, `etichetta*.fr3` | Accettazione/consegna/etichette riparazioni (A4, A5, 80 mm) | — |
| `scheda_conformita.fr3` | Dichiarazione di conformità **occhiali** | ❌ residuo del codice multi‑prodotto, non pertinente |

**Checklist MF (contenuto verificato dall'immagine del modulo):**

- Intestazione: misuratore (marca, modello, matricola) · **Tipo intervento** (messa in servizio / verificazione periodica / intervento tecnico) · **Stato sigillo** (mancante / irregolare / integro) · **Stato targhetta verde** (mancante / irregolare / scaduta / valida) · **Esito** (positivo / negativo).
- **A – Esame esteriore** (A1 etichetta fiscale, A2 libretto fiscale, A3 integrità carrozzeria/sigillo)
- **B – In assenza di sigillo o targhetta** (B1 autocertificazioni, B2–B4 test di sconnessione memoria/visore/stampante, B5 batteria tampone)
- **C – Conformità fiscale** (C1 periferiche, C2 chiusura giornaliera, C3 intestazione scontrino, C4 leggibilità, C5 coerenza matricola scontrino/libretto/etichetta, C6 rapporto fiscale)
- **D – Emissione scontrini e rapporti** (D1–D4)
- **E – Giornale di fondo elettronico** (E1–E4)
- **F – Apparecchio ambulante** (F1–F2)
- Piede: data fine intervento · **punzone fiscale (sigillo identificativo)** · **firma tecnico** · **firma utente** · durata intervento (minuti).

Ogni voce ha esito **positivo / negativo**. La struttura "sezioni → voci → esito" è ottima e va **digitalizzata** nel nuovo modulo (con voci aggiornate per gli RT).

**Firme:** solo **su carta** (spazi firma nei moduli). Nessuna firma digitale/grafometrica. **Archiviazione PDF:** esportazione manuale possibile (FastReport PDF), **nessun archivio documentale automatico** collegato alla verifica.

---

## 7. Sicurezza e qualità (rilievi) ✅/🟡

| Rilievo | Gravità |
|---|---|
| Database Access locale, nessun controllo accessi per utente sulle verifiche | Alta |
| Nessun audit log: una verifica conclusa si **modifica o elimina** liberamente | Alta |
| Password del portale tecnici salvate **in chiaro** (`pw_web`) | Alta |
| **Credenziali FTP del server del produttore scritte in chiaro nell'eseguibile** (non riportate qui) | Alta (lato produttore) |
| Query SQL costruite concatenando testo (`… where logotipo='` + valore) → fragilità/iniezione | Media |
| Dati copiati tra tabelle senza chiavi esterne → incoerenze possibili | Media |
| Backup solo manuale (copia dei file `.mdb`; esiste "compatta database") | Media |
| Nessuna firma, foto o allegato legato alla verifica | Media |

---

## 8. Cosa fa bene il vecchio programma (da non perdere)

1. **Scadenziario come schermata iniziale**, con calendario e filtri località/provincia/cliente → pianificazione dei giri per zona.
2. **Clic destro → Inserisci verifica** dalla riga in scadenza: pochissimi passaggi.
3. **Aggiornamento automatico** di ultima verifica e prossima scadenza al salvataggio.
4. **Operazioni sul dispositivo** esplicite (messa in servizio, verifica, defiscalizzazione, rimessa in servizio, **passaggio ad altro cliente**).
5. **Filtri operativi utili** (sospesi, dismessi, in garanzia, in esaurimento).
6. **Dati economici** sulla verifica (tipo contratto, prezzo, importo, pagato, fatturato) → collegamento con la fatturazione.
7. **Anagrafica tecnici con sigillo** e periodo di collaborazione.
8. **Stampe pronte** (checklist, dichiarazioni, elenchi, tagliandi).
9. **Importazione dati da file standard** per chi arriva da un altro software.
10. **Scheda riparazione** apribile dall'apparecchio (legame assistenza ↔ fiscale).

## 9. Limiti principali

1. Solo **MF**, niente RT (matricola, periodicità, QR, portale AdE).
2. **Punto vendita non modellato** (indirizzo dentro l'apparecchio).
3. **Checklist solo cartacea**, nessun esito per singola voce.
4. **Firme solo su carta**, nessun PDF archiviato automaticamente.
5. **Nessuna tracciabilità** delle modifiche, verifiche concluse modificabili/eliminabili.
6. **Monoutente/locale**; app mobile solo Android con sincronizzazione FTP manuale.
7. Anagrafica clienti separata da quella dell'assistenza (duplicazioni).
8. Nessuna notifica/promemoria al cliente per la scadenza.

---

## 10. Domande aperte per te

1. Hai ancora il PC (o un backup) con `dbvf.mdb` e `Db\Azienda.mdb` **pieni**? Fino a che anno li hai usati?
2. Hai conservato i **file trimestrali `.txt`** inviati all'AdE?
3. Usavi la **fatturazione** del programma o fatturavi altrove?
4. Usavi l'**app Android** e la sincronizzazione?
5. Il campo **"Data scadenza assistenza"** lo usavi come scadenza della verifica, del contratto, o entrambe?
6. I **tagliandi**: a cosa ti servivano in pratica?
