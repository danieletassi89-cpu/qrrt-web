# Workflow operativi — Verifiche fiscali

> Flussi proposti per desktop e mobile (PWA). Ogni flusso è descritto come **input → elaborazione → output**, con il numero di tocchi stimato. Riferimento di velocità: il vecchio programma (riga in scadenza → clic destro → verifica).

## 0. Punti di ingresso

Un tecnico arriva a una verifica da **cinque porte**, tutte portano alla stessa schermata "Verifica":

| Ingresso | Dove | Tipico |
|---|---|---|
| Dashboard › Scadenze | Ufficio/tecnico | Pianificazione |
| Agenda › Appuntamento di oggi | Tecnico | Giro programmato |
| **Scansione QR** dell'RT | Tecnico sul posto | Più veloce in assoluto |
| Scheda cliente / scheda RT | Ufficio | Richiesta telefonica |
| Ticket / accettazione | Tecnico | Verifica fatta durante un'assistenza |

---

## 1. Flusso principale — verifica periodica da scadenza (mobile)

```
Dashboard ─▶ "Scadute / 7 gg" ─▶ riga RT ─▶ [Avvia verifica]
   ─▶ Conferma dati (precompilati)        1 tocco se nulla cambia
   ─▶ Checklist per sezioni               "Tutto conforme" per sezione, tocchi solo sui KO
   ─▶ Sigillo trovato / sigillo applicato 2 tocchi (+ identificativo precompilato dal profilo tecnico)
   ─▶ Esito (proposto)                    1 tocco di conferma
   ─▶ Anteprima verbale
   ─▶ Firma tecnico ─▶ Firma cliente      (o "cliente assente" + motivo)
   ─▶ [Concludi]                          transazione: PDF + hash + archivio + scadenza + audit
   ─▶ Schermata finale: "Prossima verifica: 03/2028"
         [Invia PDF al cliente]  [Stampa etichetta QR]  [Registrata su AdE ✓]
```

| Passo | Input | Elaborazione | Output |
|---|---|---|---|
| Avvia | RT selezionato | Crea verifica `IN_CORSO` (o riprende quella pianificata), precompila tipo `PERIODICA`, tecnico = utente, checklist dal modello RT | Bozza salvata sul server |
| Dati | Eventuali correzioni (sede, referente) | Le correzioni aggiornano l'anagrafica **viva** con audit | Dati allineati |
| Checklist | OK/KO/N.A., note, foto sui KO | Salvataggio a ogni tocco; calcolo esito proposto | Checklist completa |
| Sigillo | Stato trovato, identificativo applicato | Validazione formato | Campi sigillo |
| Esito | Conferma | Se KO bloccanti ≠ esito scelto → richiesta motivazione | Esito |
| Firme | Due firme su schermo | Hash del contenuto firmato | `DA_FIRMARE` → pronta |
| Concludi | — | Numero verbale, snapshot, PDF, SHA‑256, `CONCLUSA`, nuova scadenza, chiusura appuntamento, audit | PDF in archivio, scadenza aggiornata |

**Tocchi stimati** (verifica conforme, nessun cambio dati, checklist di ~6 sezioni): **≈ 15 tocchi + 2 firme**, ~2 minuti di interazione.

## 2. Flusso QR — dall'apparecchio alla verifica

```
[Scansiona QR] ─▶ lettura payload
   ├─ RT trovato ─▶ Scheda RT rapida: cliente · sede · stato · ultima verifica · scadenza · ticket aperti
   │                  [Avvia verifica]  [Apri ticket]  [Storico]
   └─ RT non trovato ─▶ "Nuovo RT?" ─▶ censimento guidato
                          matricola dal QR ▸ cliente (ricerca per nome/P.IVA) ▸ sede ▸ modello ▸ foto targhetta
                          ─▶ [Salva e avvia verifica]
```

| Input | Elaborazione | Output |
|---|---|---|
| QR AdE dell'RT **oppure** etichetta QR TASSIUFFICIO | Estrazione matricola (QR AdE ⚪ formato da verificare) o token (etichetta) → ricerca | Scheda RT o censimento |

Riuso: la lettura QR (fotocamera + `jsQR`, oppure da foto) è la stessa già funzionante in `qrrt-web`.

## 3. Pianificazione (ufficio, desktop)

```
Dashboard ─▶ Scadenze 30/60/90 gg ─▶ filtro zona (comune/provincia) + raggruppa per cliente/sede
   ─▶ selezione multipla RT della stessa sede ─▶ [Pianifica]
   ─▶ data/ora, tecnico ─▶ appuntamento "Verifica fiscale" nell'agenda Helpdesk
        con N verifiche PIANIFICATE collegate
   ─▶ (opz.) [Avvisa cliente] email con data proposta
```

- **Spostare** l'appuntamento sposta le verifiche collegate.
- **Annullare** l'appuntamento riporta le verifiche tra le "da pianificare" (non le cancella).
- **Completare**: quando tutte le verifiche collegate sono concluse, l'appuntamento si chiude da solo.
- Viste: giorno / settimana, filtro tecnico, colore per tipo.

## 4. Registrazione rapida (verifica già fatta su carta)

Per il periodo di transizione e per le verifiche fatte senza dispositivo:

```
Scheda RT ─▶ [Registra verifica già eseguita]
   ─▶ data, tipo, esito, tecnico, sigillo, importo
   ─▶ allega scansione/foto del modulo cartaceo firmato (obbligatoria)
   ─▶ [Concludi]  → source='RAPIDA', PDF riepilogo + allegato, scadenza aggiornata
```
~30 secondi, come nel vecchio programma, senza perdere la tracciabilità.

## 5. Esito negativo

```
Esito NEGATIVO ─▶ firma ─▶ Concludi
   ─▶ RT: indicatore "esito negativo aperto", nessuna nuova scadenza
   ─▶ proposta [Crea ticket di riparazione] precompilato (RT, voci KO, foto)
   ─▶ dopo la riparazione: nuova verifica (STRAORDINARIA/PERIODICA) chiude l'indicatore
```

## 6. Verifica durante un'assistenza

```
Ticket/accettazione su cliente X ─▶ banner: "2 RT di questo cliente: 1 verifica scaduta (12/05/2026)"
   ─▶ [Esegui verifica ora] ─▶ flusso §1 con ticket collegato
```

## 7. Attivazione nuovo RT

```
Nuovo RT (da QR o manuale) ─▶ cliente/sede/modello/matricola ─▶ stato IN_MAGAZZINO
   ─▶ [Attiva] ─▶ verifica ATTIVAZIONE (checklist di attivazione) ─▶ Concludi
   ─▶ stato ATTIVO, data attivazione, prima scadenza calcolata
```

## 8. Trasferimento e dismissione

- **Trasferisci** (altro cliente o altra sede): data, motivo → nuova riga in `fiscal_rt_placements`; le verifiche passate restano legate all'RT e mostrano il cliente dell'epoca (snapshot).
- **Dismetti**: verifica `DISMISSIONE` con documento → stato `DISMESSO`, fuori da scadenze e dashboard.

## 9. Rettifica di una verifica conclusa (responsabile)

```
Verifica CONCLUSA ─▶ [Rettifica] (solo ruolo Responsabile)
   ─▶ motivo obbligatorio ─▶ modifica ─▶ nuove firme se il contenuto firmato cambia
   ─▶ PDF revisione 2 (la revisione 1 resta scaricabile) ─▶ audit
```

## 10. Registrazione su portale AdE (fase 1, manuale)

```
Verifica CONCLUSA ─▶ riquadro "Da registrare su AdE" con dati pronti da copiare (matricola, data, esito, sigillo, tecnico)
   ─▶ il tecnico registra sul portale ─▶ [Segna come registrata] data + riferimento/ricevuta (foto/screenshot)
   ─▶ esce dall'elenco "Da registrare" della dashboard
```

## 11. Chiusura della giornata (tecnico, mobile)

```
Agenda di oggi ─▶ elenco appuntamenti con stato verifiche (✓ concluse, ● in corso, ○ da fare)
   ─▶ "Da firmare/completare" e "Da registrare su AdE" in evidenza
```

---

## 12. Adattamento ai dispositivi

| Dispositivo | Uso principale | Layout |
|---|---|---|
| iPhone / Android | Verifica sul posto, QR, foto, firme | Una colonna, checklist a schede per sezione, azione primaria fissa in basso, fotocamera integrata |
| Tablet | Verifica + firma del cliente | Due colonne (checklist · dettaglio/anteprima), firma a tutto schermo in orizzontale |
| Notebook/PC | Pianificazione, anagrafiche, controllo, stampe, import | Liste con filtri, agenda settimanale, anteprima PDF |

**PWA:**
- Installabile, icona dedicata, avvio a schermo intero (come già `qrrt-web`).
- Fotocamera per QR e foto (`getUserMedia` / input file con `capture`).
- **Bozza locale** della verifica in corso: se la rete cade, i tocchi restano sul dispositivo e vengono inviati alla riconnessione; la **chiusura** avviene solo online (serve il server per numero, PDF, hash). Lotto dedicato in roadmap.
- Nessun dato fiscale in `localStorage` oltre alla bozza in corso; la bozza si cancella alla chiusura/logout.
