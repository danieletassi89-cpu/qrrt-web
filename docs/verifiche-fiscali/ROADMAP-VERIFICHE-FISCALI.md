# Roadmap — Modulo Verifiche fiscali

> Sviluppo in **lotti incrementali**, ognuno rilasciabile e reversibile. Nessun lotto parte senza tua approvazione.
> Prerequisito di tutto: **accesso al codice e allo schema di TASSIUFFICIO Helpdesk** (lotto 0).

## Panoramica

| Lotto | Obiettivo | Valore per te |
|---|---|---|
| 0 | Allineamento sull'Helpdesk reale + completamento analisi FiscalWeb21 | Progetto definitivo senza ipotesi |
| 1 | Fondamenta: sedi, apparecchiature, audit, ruoli | Base comune anche per l'assistenza |
| 2 | Parco RT + catalogo + scheda RT nel cliente | Vedi tutti gli RT dei clienti |
| 3 | Import dati (a secco, poi reale) | Niente reinserimento manuale |
| 4 | Scadenze + dashboard | Sai cosa c'è da fare |
| 5 | Verifica base (registrazione rapida) + immutabilità | Smetti di usare FiscalWeb21 per registrare |
| 6 | Checklist digitale + esito | Verifica guidata sul posto |
| 7 | Firme + PDF + archivio + invio | Documento completo senza carta |
| 8 | Agenda integrata | Pianificazione giri |
| 9 | QR + etichette | Dall'apparecchio alla verifica in un tocco |
| 10 | Collegamento ticket/accettazioni | Assistenza e fiscale uniti |
| 11 | Bozza offline + rifiniture mobile | Lavoro senza rete |
| 12 | Report, export, fatturazione | Controllo e amministrazione |

Ordine flessibile dopo il lotto 5 (es. QR prima dell'agenda se ti serve prima).

---

## Lotto 0 — Allineamento
- **Obiettivo:** sostituire le ipotesi con la realtà.
- **Funzioni:** lettura codice/schema Helpdesk; navigazione guidata FiscalWeb21; raccolta checklist RT ufficiale, regola scadenza, payload QR reali, esempio export FW21.
- **DB:** nessuna modifica.
- **Backend/Frontend:** nessuno.
- **Test:** —
- **Accettazione:** documenti aggiornati (analisi FW21 completa, data model con tabelle reali) e da te approvati.
- **Rischi:** export FW21 incompleto → migrazione più manuale.
- **Rollback:** n/a.

## Lotto 1 — Fondamenta comuni
- **Obiettivo:** strutture che servono a tutto l'Helpdesk.
- **Funzioni:** sedi/punti vendita del cliente (se mancano); apparecchiature del cliente (se mancano); audit log generale; ruoli/permessi "fiscali".
- **DB:** `hd_customer_sites`, `hd_assets`, `hd_audit_events` (solo quelle mancanti); colonna `asset_id` su ticket/accettazioni.
- **Backend:** CRUD sedi/apparecchiature con validazione server‑side; servizio di audit trasversale; controlli di permesso.
- **Frontend:** sezione "Sedi" e "Apparecchiature" nella scheda cliente (stile restyling, icone SVG).
- **Test:** unitari su validazioni e permessi; migrazione su copia DB; audit generato per ogni modifica.
- **Accettazione:** creo una sede e un'apparecchiatura, le vedo nel cliente, l'audit registra chi/quando/cosa.
- **Rischi:** conflitto con strutture simili già esistenti → risolto nel lotto 0.
- **Rollback:** migrazioni reversibili (down), funzioni dietro **flag di attivazione**; nessun dato esistente modificato.

## Lotto 2 — Parco RT
- **Obiettivo:** anagrafica RT unica.
- **Funzioni:** catalogo produttori/modelli; dettaglio RT (matricola validata, stato, date, contratto); trasferimento; riquadro "Fiscale" nella scheda cliente; scheda RT con timeline (per ora: dati + trasferimenti).
- **DB:** `device_manufacturers`, `device_models`, `fiscal_rt_devices`, `fiscal_rt_placements`, `fiscal_lab_settings`, `fiscal_technician_profiles`.
- **Backend:** API RT con unicità matricola, transizioni di stato consentite, storico trasferimenti.
- **Frontend:** elenco RT con ricerca (matricola, cliente, comune) e filtri (attivi, fuori servizio, dismessi, in garanzia); scheda RT; impostazioni laboratorio e profili tecnici.
- **Test:** matricole valide/non valide/duplicate; trasferimento mantiene storico; permessi.
- **Accettazione:** inserisco un RT in < 1 minuto; aprendo il cliente vedo i suoi RT con stato.
- **Rischi:** formato matricola con eccezioni → validazione configurabile + forzatura motivata.
- **Rollback:** flag modulo off; tabelle nuove eliminabili senza impatto sul resto.

## Lotto 3 — Import
- **Obiettivo:** portare dentro i dati esistenti.
- **Funzioni:** import vecchio programma (`.mdb` → CSV), import FW21 (formato da lotto 0), eventuale import file trimestrali; anteprima, conflitti, conferma, annullamento batch.
- **DB:** `import_batches`, `import_rows`; `legacy_ref` sulle entità.
- **Backend:** pipeline §3 del documento migrazione, transazioni per batch.
- **Frontend:** procedura guidata a 4 passi (carica → anteprima → risolvi conflitti → conferma), report scaricabile.
- **Test:** con copie reali dei tuoi dati su ambiente di prova; controlli §6; import ripetuto non crea duplicati.
- **Accettazione:** 10 RT a campione identici a FW21; conteggi coincidenti; tu approvi il report.
- **Rischi:** qualità dati di partenza; clienti omonimi → coda "da verificare".
- **Rollback:** annullamento del batch (elimina solo ciò che il batch ha creato); backup prima della conferma in produzione.

## Lotto 4 — Scadenze e dashboard
- **Obiettivo:** vedere subito cosa fare.
- **Funzioni:** regola di scadenza configurabile; dashboard (oggi, scadenze per fasce, da sistemare, ultime); liste filtrate per zona/tecnico; export elenco.
- **DB:** indici su scadenza; nessuna tabella nuova.
- **Backend:** calcolo scadenza centralizzato; job notturno di coerenza.
- **Frontend:** dashboard desktop e mobile, contatori cliccabili.
- **Test:** calcolo scadenze su casi limite (fine mese, 29 febbraio, esito negativo); numeri uguali a FW21 alla stessa data.
- **Accettazione:** la dashboard mostra gli stessi RT in scadenza che vedi in FW21.
- **Rischi:** regola di scadenza diversa da quella reale → confermata nel lotto 0.
- **Rollback:** flag off della dashboard; dati non toccati.

## Lotto 5 — Verifica base e immutabilità
- **Obiettivo:** registrare le verifiche nell'Helpdesk.
- **Funzioni:** stati della verifica; registrazione rapida con allegato scansione; chiusura transazionale; aggiornamento scadenza; blocco post‑chiusura; rettifica e annullamento motivati; promemoria "da registrare su AdE".
- **DB:** `fiscal_checks`, `fiscal_check_documents`, `fiscal_check_revisions`; trigger di immutabilità.
- **Backend:** macchina a stati, transazione di chiusura, numerazione verbali, controlli tecnico abilitato alla data.
- **Frontend:** "Avvia/Registra verifica" da dashboard e scheda RT; storico verifiche nella scheda RT e cliente.
- **Test:** tentativi di modifica dopo chiusura (API e DB) rifiutati; rettifica crea revisione; rollback di chiusura fallita; audit completo.
- **Accettazione:** registro una verifica in ~30 secondi; non riesco a modificarla senza rettifica; la scadenza si aggiorna.
- **Rischi:** processi reali che richiedono correzioni frequenti → rettifica semplice ma tracciata.
- **Rollback:** flag off; le verifiche già registrate restano consultabili (sola lettura).

## Lotto 6 — Checklist digitale
- **Obiettivo:** verifica guidata sul posto.
- **Funzioni:** modelli checklist versionati; compilazione per sezioni con "tutto conforme"; foto sui KO; esito proposto; voci per ambulanti.
- **DB:** `fiscal_checklist_templates`, `fiscal_checklist_template_items`, `fiscal_check_answers`.
- **Backend:** salvataggio incrementale, calcolo esito, blocco della versione del modello.
- **Frontend:** checklist mobile first, grandi pulsanti OK/KO/N.A.
- **Test:** cambio modello non altera verifiche passate; KO bloccante propone negativo; salvataggio a ogni tocco.
- **Accettazione:** una verifica conforme si completa in ~2 minuti da iPhone.
- **Rischi:** checklist troppo lunga → rivista con te sul campo.
- **Rollback:** la registrazione rapida (lotto 5) resta disponibile.

## Lotto 7 — Firme, PDF, archivio, invio
- **Obiettivo:** documento finale senza carta.
- **Funzioni:** firma tecnico/cliente su schermo; cliente assente; PDF rapporto; hash; archivio immutabile; invio email con registro; download in blocco.
- **DB:** `fiscal_check_signatures`; `sha256`/`immutable` su allegati.
- **Backend:** generazione PDF lato server, calcolo e verifica hash, invio email in coda.
- **Frontend:** anteprima, pad di firma, schermata finale con azioni.
- **Test:** PDF identico a parità di dati; hash verificato al download; invio solo su conferma; firme non accessibili da URL pubblico.
- **Accettazione:** il cliente riceve il PDF firmato; lo ritrovo dallo storico anni dopo.
- **Rischi:** requisiti legali sulla firma → firma elettronica semplice, valutare in seguito soluzioni avanzate.
- **Rollback:** flag off della firma digitale → torna la registrazione rapida con scansione.

## Lotto 8 — Agenda integrata
- **Obiettivo:** pianificare senza un secondo calendario.
- **Funzioni:** tipo appuntamento "Verifica fiscale"; più RT per appuntamento; sposta/annulla/completa sincronizzati; vista giorno/settimana per tecnico; avviso al cliente (opzionale).
- **DB:** `type` su appuntamenti; `fiscal_check_appointments`.
- **Backend:** sincronizzazione stati appuntamento↔verifiche.
- **Frontend:** pianificazione multipla dalla lista scadenze; agenda del tecnico su mobile.
- **Test:** annullo appuntamento → verifiche tornano da pianificare; completamento automatico.
- **Accettazione:** pianifico un giro di 5 clienti di un comune in pochi minuti.
- **Rischi:** agenda esistente poco estendibile → valutato nel lotto 0.
- **Rollback:** flag off; appuntamenti restano appuntamenti generici.

## Lotto 9 — QR ed etichette
- **Obiettivo:** dall'apparecchio alla verifica in un tocco.
- **Funzioni:** scansione QR RT (riuso logica `qrrt-web`); censimento da QR; token/etichetta QR TASSIUFFICIO; stampa su BIXOLON con prossima scadenza.
- **DB:** `public_token` su apparecchiature; `qr_payload` su RT.
- **Backend:** risoluzione token (solo utenti autenticati); parser del payload QR AdE.
- **Frontend:** pulsante "Scansiona" sempre disponibile su mobile.
- **Test:** QR reali (anche foto); token non indovinabili; accesso negato senza login.
- **Accettazione:** scansiono un RT e apro la sua scheda in < 3 secondi.
- **Rischi:** formati QR diversi per produttore → parser tollerante + ricerca manuale.
- **Rollback:** flag off; la ricerca per matricola resta.

## Lotto 10 — Assistenza ↔ fiscale
- **Obiettivo:** un solo storico per l'apparecchio.
- **Funzioni:** timeline unica RT (verifiche + ticket + accettazioni); avviso scadenza nel ticket; ticket da esito negativo; verifica da ticket.
- **DB:** nessuna nuova tabella (usa `asset_id`).
- **Backend/Frontend:** banner e azioni nei ticket; timeline.
- **Test:** avvisi corretti su clienti con/senza RT scaduti.
- **Accettazione:** aprendo un ticket vedo se l'RT è da verificare e lo verifico nello stesso intervento.
- **Rischi:** avvisi troppo invadenti → solo se scadenza ≤ 30 gg, chiudibili.
- **Rollback:** flag off degli avvisi.

## Lotto 11 — Offline e rifiniture mobile
- **Obiettivo:** lavorare anche senza campo.
- **Funzioni:** bozza locale della verifica, coda di invio, indicatori di sincronizzazione; chiusura solo online.
- **DB:** nessuna.
- **Backend:** API idempotenti (id client) per evitare doppi invii.
- **Frontend:** service worker, stato "salvato sul telefono / inviato".
- **Test:** perdita rete a metà checklist; doppio invio; logout cancella bozze.
- **Accettazione:** completo la checklist in un locale senza rete e chiudo appena torna.
- **Rischi:** conflitti se due dispositivi modificano la stessa bozza → un solo dispositivo "proprietario" della verifica in corso.
- **Rollback:** disattivazione offline, resta il funzionamento online.

## Lotto 12 — Report, export, fatturazione
- **Obiettivo:** controllo amministrativo.
- **Funzioni:** report per periodo/tecnico/esito/zona; export Excel/CSV/PDF; elenco "da fatturare" ed export verso il sistema di fatturazione in uso.
- **DB:** eventuali viste.
- **Test:** totali coerenti con i dati.
- **Accettazione:** a fine mese esporto l'elenco delle verifiche da fatturare.
- **Rischi:** formato del gestionale di fatturazione → da definire.
- **Rollback:** funzioni in sola lettura, nessun impatto sui dati.

---

## Regole comuni a ogni lotto

- Sviluppo su branch dedicato, revisione, **ambiente di prova con copia dei dati**.
- Migrazioni DB **reversibili** e **backup** prima di ogni rilascio.
- Ogni funzione dietro **flag di attivazione** per spegnerla senza rilasciare di nuovo.
- Test automatici (unitari + integrazione) sui punti critici: validazioni, permessi, transazioni, immutabilità.
- Verifica di accessibilità e resa su iPhone, Android, tablet e PC prima del rilascio.
- Nessun dato reale modificato senza la tua conferma.
