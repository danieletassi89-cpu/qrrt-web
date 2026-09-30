# Progetto — Modulo "Verifiche fiscali" per TASSIUFFICIO Helpdesk

> **Proposta preliminare da approvare.** Nessuno sviluppo avviato.
> Basata su: analisi del vecchio programma (verificata), conoscenza normativa pubblica (da riverificare), app **TASSIUFFICIO QR RT** (repository `qrrt-web`, letto).
> ⚠️ **Il codice di TASSIUFFICIO Helpdesk non è disponibile in questa sessione**: le parti di integrazione sono scritte sulle entità che un Helpdesk di assistenza tecnica ha tipicamente (clienti, ticket, accettazioni, appuntamenti, utenti, allegati). Vanno confermate sul codice reale prima della progettazione definitiva (vedi §12).

---

## 1. Obiettivo

Gestire in TASSIUFFICIO Helpdesk l'intero ciclo delle verifiche periodiche dei registratori telematici:

```
censimento RT → scadenza → pianificazione → verifica guidata → esito → firma → PDF → archivio → registrazione AdE → prossima scadenza
```

con **un'unica anagrafica cliente**, **una sola agenda**, **lo stesso strumento su PC e smartphone**, e **tracciabilità completa**.

### Principi guida

1. **Niente dati doppi.** Cliente, sede, contatti, utenti, agenda e allegati sono quelli dell'Helpdesk. Il modulo aggiunge solo ciò che è fiscale.
2. **Veloce come il vecchio programma.** Dalla scadenza alla verifica in un tocco; checklist "tutto OK, tocco solo le eccezioni".
3. **Mobile first per il tecnico, desktop per l'ufficio.**
4. **Una verifica conclusa è un documento**, non un record modificabile.
5. **Ogni funzione nuova deve far risparmiare tempo o evitare un errore.**

---

## 2. Perimetro

### Dentro
- Parco RT dei clienti (censimento, stato, trasferimenti, storico).
- Catalogo produttori/modelli.
- Profilo fiscale dei tecnici (abilitazione, sigillo/punzone).
- Dati del laboratorio.
- Verifiche (tipi, stati, checklist, esito, sigillo, firme, PDF, archivio).
- Scadenze e dashboard.
- Appuntamenti "Verifica fiscale" nell'agenda esistente.
- Etichetta/lettura QR.
- Import dati storici.

### Fuori (restano all'Helpdesk o ad altri sistemi)
- Anagrafica clienti, sedi, contatti (Helpdesk).
- Riparazioni/ticket/accettazioni (Helpdesk — il modulo si **collega**).
- Fatturazione (sistema attuale — il modulo **segnala/esporta** "da fatturare").
- Comunicazione automatica all'Agenzia: **non nel primo rilascio** (vedi §9).

---

## 3. Modello concettuale e integrazione

```
CLIENTE (Helpdesk)
  └── SEDE / PUNTO VENDITA (Helpdesk; da introdurre se non esiste)
        └── APPARECCHIATURA (generica, condivisa con i ticket)
              └── dettaglio RT (dati fiscali: matricola, modello, stato fiscale, attivazione, QR)
                    ├── VERIFICHE FISCALI ──> checklist, esito, sigillo, firme, documenti
                    ├── TICKET / ACCETTAZIONI (Helpdesk, collegati all'apparecchiatura)
                    ├── APPUNTAMENTI (agenda Helpdesk, tipo "Verifica fiscale")
                    └── SCADENZA (calcolata dall'ultima verifica valida)
```

### 3.1 Cosa è condiviso e cosa è solo fiscale

| Dato | Proprietario | Motivo |
|---|---|---|
| Ragione sociale, P.IVA, CF, indirizzi, contatti | **Helpdesk (cliente)** | Già usati da ticket e accettazioni |
| Sede/punto vendita (insegna, indirizzo, referente, orari) | **Helpdesk (sede)** | Serve anche ai ticket e agli appuntamenti |
| Marca, modello, seriale, ubicazione dell'apparecchio | **Helpdesk (apparecchiatura)** | Un RT si ripara anche: lo stesso oggetto deve comparire nei ticket |
| Matricola fiscale, tipo dispositivo, data attivazione, stato fiscale, URL QR | **Modulo fiscale (dettaglio RT)** | Ha senso solo per l'adempimento |
| Verifiche, checklist, esiti, sigilli, firme, verbali | **Modulo fiscale** | Documenti con valore legale, regole di immutabilità proprie |
| Tecnico (utente, nome, login) | **Helpdesk (utente)** | Un solo account |
| Abilitazione, identificativo sigillo/punzone, periodo | **Modulo fiscale (profilo tecnico)** | Dati regolamentati |
| Appuntamento | **Helpdesk (agenda)** con tipo "verifica" e collegamento alla verifica | Un solo calendario |
| File (PDF, foto) | **Archivio allegati Helpdesk** con metadati fiscali e hash | Un solo sistema di file e backup |
| Prezzo/importo | Modulo fiscale (verifica) | Il resto (fattura) fuori |

**Snapshot:** alla chiusura della verifica i dati di cliente, sede, RT e tecnico vengono **fotografati** dentro la verifica (come faceva, correttamente, il vecchio programma). Il verbale resta identico anche se domani il cliente cambia indirizzo; le anagrafiche vive restano uniche.

### 3.2 Scheda cliente nell'Helpdesk — nuova sezione "Fiscale"

Aprendo un cliente, oltre a dati, sedi, ticket e accettazioni esistenti, compare (solo se ha RT) un riquadro:

| RT | Sede | Modello | Stato | Ultima verifica | Prossima | Azioni |
|---|---|---|---|---|---|---|
| 99XXX000000 | Bar Centrale – Via Roma | Produttore Modello | ● Attivo | 12/03/2025 ✓ | **03/2027** | Verifica · Storico · QR |

Cliccando un RT si apre la **scheda RT** con la **timeline unica**: attivazione, verifiche (con PDF), ticket, trasferimenti, note, documenti, appuntamenti.

---

## 4. Tipi di intervento e stati

### 4.1 Tipi di intervento fiscale (⚪ da validare con te e con la prassi AdE)

| Codice | Descrizione | Effetto sulla scadenza |
|---|---|---|
| `ATTIVAZIONE` | Messa in servizio/attivazione con prima verificazione | Nuova scadenza = data + periodicità |
| `PERIODICA` | Verificazione periodica | Nuova scadenza = data + periodicità (se esito positivo) |
| `STRAORDINARIA` | Intervento con rimozione/riapposizione sigillo (es. dopo riparazione) | Configurabile: di norma riavvia il periodo ⚪ |
| `DISMISSIONE` | Messa fuori servizio/dismissione | Nessuna scadenza, RT esce dal parco attivo |

Il vecchio tipo "messa in servizio **e** verifica periodica" diventa semplicemente `ATTIVAZIONE`.

### 4.2 Ciclo di vita di una verifica

```
PIANIFICATA ──> IN CORSO ──> DA FIRMARE ──> CONCLUSA ──> (REGISTRATA AdE)
     │              │             │             │
     └─> ANNULLATA  └─> ANNULLATA └─> IN CORSO  └─> RETTIFICATA (nuova versione, motivo obbligatorio)
```

| Stato | Chi | Modificabile | Note |
|---|---|---|---|
| Pianificata | ufficio/tecnico | sì | Nasce dall'agenda o dalla dashboard |
| In corso | tecnico | sì | Checklist in compilazione, bozza salvata di continuo |
| Da firmare | tecnico | solo tornando "in corso" | Anteprima PDF |
| **Conclusa** | sistema | **no** | PDF generato, hash calcolato, scadenza aggiornata |
| Registrata AdE | tecnico/ufficio | solo i campi di registrazione | Data + riferimento/ricevuta |
| Rettificata | responsabile | no | La versione precedente resta visibile e scaricabile |
| Annullata | responsabile | no | Solo prima della chiusura, con motivo |

### 4.3 Stato dell'RT

`IN_MAGAZZINO` → `ATTIVO` → (`FUORI_SERVIZIO` ↔ `ATTIVO`) → `DISMESSO`
Più indicatori calcolati: *verifica scaduta*, *in scadenza*, *dati incompleti*, *esito negativo aperto*.

---

## 5. Checklist

- **Modelli di checklist versionati** (es. "RT – verificazione periodica v1"): sezioni → voci → tipo risposta.
- Contenuto iniziale: basato sulle **prove minime AdE per gli RT** (documento da acquisire) e sulla struttura A–F del vecchio modulo MF (esame esteriore, sigillo, conformità, emissione documenti, trasmissione, ambulanti).
- Tipi di risposta: **OK / KO / N.A.**, testo, numero, foto obbligatoria su KO (configurabile).
- **Velocità**: pulsante "Tutto conforme" per sezione; si toccano solo le eccezioni. Voci non applicabili nascoste in base al modello (es. ambulante).
- **Esito proposto** automaticamente: un KO su voce "bloccante" → esito negativo. Il tecnico conferma.
- Una verifica conserva **la versione della checklist** con cui è stata eseguita: cambiare il modello non altera le verifiche passate.

### Dati strutturati della verifica (oltre alla checklist)

Stato sigillo trovato (integro/assente/manomesso) · sigillo applicato (identificativo) · stato QR/libretto · versione firmware ⚪ · note · foto (targhetta, sigillo, scontrino di prova) · durata · importo · pagato/da fatturare.

---

## 6. Firme e documenti

### 6.1 Flusso

```
checklist completa → anteprima verbale → firma tecnico → firma cliente (o "cliente assente" + motivo)
  → generazione PDF → hash SHA-256 → archiviazione (verifica + RT + cliente) → [invio email su conferma]
```

### 6.2 Documenti generati

| Documento | Quando | Contenuto |
|---|---|---|
| **Rapporto di verificazione** (PDF A4) | Chiusura | Laboratorio, tecnico e sigillo, cliente/sede, RT, tipo intervento, checklist con esiti, esito, sigillo applicato, prossima scadenza, firme, codice verifica + QR di controllo |
| Dichiarazione di attivazione / dismissione ⚪ | Se richiesta dal tipo intervento | Modello da confermare |
| **Etichetta QR** (35×70 mm, BIXOLON) | Chiusura (facoltativa) | QR TASSIUFFICIO + matricola + prossima scadenza |
| Elenchi (PDF/Excel) | A richiesta | Scadenze, verifiche per periodo/tecnico |

### 6.3 Firma

- **Firma su schermo** (dito o penna) su telefono/tablet; su PC con mouse o passando il dispositivo al cliente.
- Salvata come immagine vettoriale/PNG **dentro il PDF**, più: nome del firmatario, data/ora, utente che ha raccolto la firma, hash del documento firmato.
- È una **firma elettronica semplice**: adeguata come prova di consegna/presa visione. ⚪ Se servisse valore di firma avanzata/qualificata, va valutato un servizio esterno (fuori dal primo rilascio).

### 6.4 Archivio

- PDF salvati nell'archivio allegati dell'Helpdesk, **mai sovrascritti** (una rettifica genera un nuovo PDF, il vecchio resta).
- Ricerca per cliente, RT, matricola, data, tecnico, esito.
- Scaricabili singolarmente o in blocco (es. tutte le verifiche di un cliente/anno).

### 6.5 Invio al cliente

- Email con PDF (o link a scadenza), **sempre dopo conferma** del tecnico/ufficio.
- Registro invii (a chi, quando, esito).

---

## 7. Scadenze, dashboard, agenda

### 7.1 Regola di scadenza
- Parametro di configurazione: **periodicità RT = 24 mesi** ⚪ (confermare la regola esatta: da data verifica, fine mese, ecc.).
- Calcolata **dalla verifica conclusa con esito positivo** più recente; mai digitata a mano (eccezione: import storico e correzione motivata da responsabile).
- MF importati: storico consultabile, nessuna scadenza attiva.

### 7.2 Dashboard "Verifiche fiscali"

Poche informazioni, tutte cliccabili verso una lista filtrata:

```
┌ OGGI ─────────────────┐ ┌ SCADENZE ─────────────────────────────┐
│ 3 verifiche in agenda │ │ Scadute 4 · 7gg 6 · 30gg 18 · 90gg 41 │
│ 1 da completare/firm. │ │ [filtro zona ▾] [filtro tecnico ▾]    │
└───────────────────────┘ └───────────────────────────────────────┘
┌ DA SISTEMARE ─────────────────────────┐ ┌ ULTIME ───────────────┐
│ 2 esiti negativi aperti               │ │ 5 verifiche concluse  │
│ 3 verifiche non registrate su AdE     │ │   (ultimi 7 giorni)   │
│ 7 RT con dati incompleti              │ └───────────────────────┘
└───────────────────────────────────────┘
```

- "RT senza prossima verifica" e "dati incompleti" confluiscono in **Da sistemare** (sono lo stesso problema per l'utente).
- Lista scadenze ordinabile per **comune/zona** (per organizzare i giri, come nel vecchio programma), con azioni rapide: **Pianifica**, **Avvia verifica**, **Chiama**.

### 7.3 Agenda
- **Nessuna agenda nuova**: si estende quella dell'Helpdesk con il tipo "Verifica fiscale" collegato a (cliente, sede, uno o più RT).
- Da agenda: *pianifica · assegna tecnico · sposta · avvia · completa · annulla*, viste giorno/settimana, filtro tecnico.
- Pianificare più RT della stessa sede in **un solo appuntamento**.
- Completare la verifica chiude l'appuntamento; annullare l'appuntamento riporta la verifica tra le "da pianificare".
- ⚪ Se l'agenda Helpdesk non supporta tipi/collegamenti, è la prima estensione da fare (lotto dedicato).

---

## 8. QR code

Due QR con ruoli diversi:

1. **QR dell'RT (Agenzia)** — già letto dall'app **TASSIUFFICIO QR RT**. Scansionandolo dal modulo: si ricava la **matricola** ⚪ (da verificare il contenuto esatto del payload con alcuni QR reali) → apertura diretta della scheda RT; se l'RT non esiste → *censimento guidato* precompilato.
2. **Etichetta QR TASSIUFFICIO** (stampata con la BIXOLON SLP‑TX220B già configurata in `qrrt-web`): contiene un link alla scheda RT nell'Helpdesk (identificativo non indovinabile, accesso solo autenticato). Utile anche per l'assistenza (apertura ticket dall'apparecchio).

**Flusso QR:** scansiona → scheda RT (cliente, sede, stato, ultima verifica, scadenza, ticket aperti) → **Avvia verifica** / **Apri ticket**.

---

## 9. Rapporto con l'Agenzia delle Entrate

- Fase 1 (realistica): il modulo **non comunica** con l'AdE. Dopo la chiusura mostra il promemoria "**Registra l'esito sul portale AdE**", con i dati pronti da copiare, e un campo per **data registrazione + ricevuta/screenshot**. La dashboard evidenzia le verifiche concluse non ancora registrate.
- Fase successiva (solo se fattibile): automazione tramite servizi ufficiali, se disponibili e utilizzabili dal laboratorio. Da studiare dopo aver visto come lavora oggi FiscalWeb21.

---

## 10. Collegamento assistenza ↔ verifiche (funzioni nuove ad alto valore)

| Situazione | Comportamento |
|---|---|
| Apro un **ticket** su un cliente che ha RT **scaduti o in scadenza ≤ 30 gg** | Avviso nel ticket: "RT … verifica scaduta il …" + pulsante *Pianifica verifica nello stesso intervento* |
| **Esito negativo** | Proposta di creare un ticket di riparazione precompilato (RT, problema dalle voci KO, foto) |
| Riparazione che **rompe il sigillo** | Il ticket chiede se serve un intervento `STRAORDINARIO` |
| **Accettazione** di un RT in laboratorio | L'RT viene riconosciuto (matricola/QR) e il suo storico è visibile |

---

## 11. Interfaccia

Coerente con il restyling approvato dell'Helpdesk (palette già usata anche in `qrrt-web`):

| Elemento | Valore di riferimento |
|---|---|
| Fondo | grigio/azzurro chiarissimo (`#F4F9FF` in qrrt-web) |
| Testo | antracite (`#282E37`) |
| Selezioni / riferimenti principali | blu notte (`#142348`) |
| Azioni primarie | corallo (`#EB5B53`) |
| Stati | verde conforme, ambra in scadenza, rosso scaduto/negativo — **sempre con icona + testo**, mai solo colore |
| Forme | angoli 14–18 px, ombre leggere, card |
| Icone | **SVG** da una libreria affidabile e con licenza libera (proposta: **Lucide**, ISC) o SVG originali; nessuna immagine raster copiata |

Da mobile: pulsanti grandi (≥ 44 px), una colonna, azione primaria sempre in basso a portata di pollice, checklist a schede per sezione, fotocamera per QR e foto. Nessun elemento grafico ripreso da FiscalWeb21.

---

## 12. Sicurezza e tracciabilità

| Requisito | Soluzione |
|---|---|
| Ruoli | *Amministratore*, *Responsabile laboratorio* (rettifiche, annullamenti, configurazione), *Tecnico abilitato* (esegue e firma), *Ufficio* (anagrafiche, agenda, consultazione), *Sola lettura* |
| Tecnico abilitato | Può concludere verifiche solo se ha profilo fiscale attivo alla data della verifica |
| Audit log | Ogni creazione/modifica/cambio stato: chi, quando, da dove, valori prima/dopo. Tabella in sola aggiunta |
| Immutabilità | Verifica conclusa bloccata a livello **server e database**; correzioni solo tramite rettifica con motivo |
| Integrità documenti | SHA‑256 del PDF salvato in DB; verifica dell'hash al download |
| Firme | Immagini firma accessibili solo tramite la verifica, mai con URL pubblico |
| Web | Protezione CSRF, escape/sanitizzazione output (XSS), Content Security Policy, validazione **server‑side** di ogni campo (matricola, date, stati) |
| Database | Query parametrizzate, transazioni per le operazioni composte (chiusura = verifica + scadenza + documento + audit), vincoli e chiavi esterne |
| Allegati | Tipi ammessi e dimensione massima, nomi file generati dal server, storage fuori dalla cartella pubblica |
| Backup/restore | Backup automatico giornaliero di DB **e** allegati, conservazione a rotazione, **prova di ripristino** documentata |
| Privacy | Dati personali minimi (i dati di nascita dei tecnici solo se richiesti), accessi tracciati |

---

## 13. Da confermare prima della progettazione definitiva

1. **Accesso al codice di TASSIUFFICIO Helpdesk** (repository, stack tecnologico, database): serve per sostituire le ipotesi di integrazione con tabelle reali.
2. Esiste già nell'Helpdesk: **sede/punto vendita**? **apparecchiature** dei clienti? **agenda** con tipi? **allegati**? **ruoli**?
3. Come registri oggi l'esito sul portale AdE e cosa fa per te FiscalWeb21 in quel passaggio.
4. Checklist RT che usi oggi (quella di FiscalWeb21 o il documento AdE sulle prove minime).
5. Regola esatta di scadenza che applichi (24 mesi dalla data? fine mese?).
6. Come fatturi le verifiche oggi.
7. Esempi reali di **payload del QR RT** (anche oscurati) per il riconoscimento della matricola.
