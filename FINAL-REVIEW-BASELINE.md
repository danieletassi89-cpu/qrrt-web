# FINAL-REVIEW-BASELINE — TASSIUFFICIO Helpdesk v1.59.4

Revisione finale pre-produzione, **fase 0: baseline**. Data: 29/09/2026.

Regole seguite in questa fase:
- nessun file del progetto è stato modificato;
- nessuna dipendenza è stata aggiornata;
- nessun database, container o configurazione reale è stato toccato.

Tutto il lavoro è stato fatto su una copia estratta in un'area temporanea isolata (scratchpad della sessione). Il database era una MariaDB 10.11 usa-e-getta, in un container dedicato (`th-test-db`, porta 127.0.0.1:33306) e senza alcun legame con l'installazione reale.

I report precedenti **non** sono stati presi per buoni. Ogni dato qui sotto viene da un'esecuzione o da una lettura diretta del codice. Dove un punto è un'ipotesi, è scritto esplicitamente.

Legenda severità: 🔴 CRITICO · 🟠 ALTO · 🟡 MEDIO · 🟢 BASSO · ℹ️ INFORMATIVO

---

## A. Versione verificata

**Esito: la baseline è v1.59.4.** Non ci sono incongruenze nei punti che determinano la versione a runtime.

### Pacchetto analizzato

- File consegnato: `d5dc96b3-consegna-v1.59.4.zip`, che contiene:
  - `tassiufficio-helpdesk-v1.59.4.zip`
  - `.sha256`
  - `report-v1.59.4.md`
- SHA-256 dell'archivio interno: `2d1daccec2ea9eaf58d74c42b5893f55605eea39277a0ba97856a460e4b3b1f9`. **Coincide** con il file `.sha256`, verificato con `sha256sum`.
- Contenuto: 380 voci, di cui 345 file.

### Dove compare la versione

| Punto | Valore | Ruolo | Esito |
|---|---|---|---|
| `backend/package.json:3` | `1.59.4` | versione applicativa; `systemStatus.controller.js:13` la mostra in Impostazioni → Stato sistema | ✅ |
| `backend/package-lock.json:3,9` | `1.59.4` | lockfile | ✅ |
| `frontend/service-worker.js:33` | `tassi-shell-v1.59.4` | cache della PWA, da cambiare a ogni consegna | ✅ |
| `CHANGELOG.md:1` | `[1.59.4] - 2026-09-25` | ultima voce | ✅ |
| `docs/PROVA-DISASTER-RECOVERY.md:1,17` | v1.59.4 | documento della prova DR | ✅ |
| Nome dello zip e del `.sha256` | v1.59.4 | consegna | ✅ |
| `frontend/manifest.json` | nessun campo versione | — | ℹ️ normale |

### Riferimenti a versioni precedenti (non sono incongruenze)

Sono commenti storici che indicano in quale versione è nata una modifica:
- `v1.59.0`–`v1.59.2` in `style.css`, `common.js`, `signatureImage.js`, `acceptances.controller.js`, `app.js`;
- `database/schema-reference.sql:353` (v1.59.1);
- `docs/DIAGNOSI-TEST-BACKUP.md:4` (v1.59.3);
- `docs/CODICE-MORTO-MAPPA.md:1` (v1.59.2).

### Incongruenze documentali (ℹ️)

- `README.md:5` descrive ancora lo stato come "FASE 2" e parla di "stati configurabili con timeline ed emoji". Oggi gli stati usano icone SVG.
- `docs/TESTING.md` dice che basta "Node 20.6+". Invece `package.json` richiede `"engines": {"node": ">=24.0.0"}`, e l'immagine Docker è `node:24-alpine`.

---

## B. Commit / branch

**🟠 La v1.59.4 non è tracciabile a un commit.**

- Lo zip consegnato **non contiene una cartella `.git`**: non esistono branch, commit, tag o storico verificabili.
- Il repository collegato alla sessione (`danieletassi89-cpu/qrrt-web`, branch `claude/epic-gates-uq2bcg`, HEAD `d07f0fe`) contiene **un'altra applicazione**: "TASSIUFFICIO QR RT", una PWA di stampa QR per BIXOLON fatta di 5 file. Non contiene l'Helpdesk.
  - Stato: `working tree clean`.
  - Commit: `39b382b` → `da38250` → `d07f0fe`.
- `report-v1.59.4.md` afferma che la v1.59.3 "resta al commit `fd64608` (tag `lotto-7`)". **Non è verificabile**: quel repository non è disponibile.

**Identificatore della baseline usato in questo documento: SHA-256 `2d1daccec2ea…b3b1f9` dello zip `tassiufficio-helpdesk-v1.59.4.zip`.**

---

## C. Architettura (ricostruita dal codice)

```
Browser / PWA (desktop, iPhone, Android)
   │  HTTP in LAN (HTTPS facoltativo: COOKIE_SECURE)
   ▼
container "app"  node:24-alpine — Express 4 (backend/server.js → src/app.js), porta 3000 → APP_PORT (8080)
   ├─ serve il frontend statico (/frontend, niente build: HTML + CSS + JS vanilla)
   ├─ /api/*            REST (CSRF, rate limit, sessione)
   ├─ /public-status/*  pagina di stato pubblica tramite QR (token)
   ├─ uploads           volume uploads_data → /app/uploads
   └─ backups           bind mount in SOLA LETTURA (solo per la pagina "stato sistema")
   │  rete docker interna
   ▼
container "db"  mariadb:10.11 (volume dedicato, non esposto)
```

### Backend

`backend/src` contiene circa 12.970 righe:
- `config/`: env, db, session, trustProxy, controlloAvvio;
- `middleware/`: security, auth, originPolicy, errorHandler;
- `routes/`: 17 file;
- `controllers/`: 21;
- `services/`: pdf, qrcode, sla, pinAuth, deviceAuth, attachments, signatureImage, publicStatus, numerazioni, provider demo clienti e apparecchiature;
- `utils/`: csv, auditLog, numerazioneConcorrente;
- `scripts/`: createAdmin, resetAdminPin, productionCheck, controllaEnv, seedDemo, verifiche;
- `db/`: 51 migrazioni knex e 9 seed.

### Frontend

In `frontend/` ci sono circa 11.975 righe HTML/JS, più `style.css` (265 KB):
- `pages/`: 17 pagine;
- `public/status.html`: pagina pubblica autonoma;
- `js/`: `common.js`, `api.js`, `icons.js`, `operatorSwitch.js`, `pwa.js`, `tema.js`.

Non ci sono dipendenze npm né librerie da CDN.

### PWA

- `manifest.json` con 4 icone (192/512, normali e maskable), 3 scorciatoie e 11 schermate di avvio iOS (`pwa.js:65-74`).
- `service-worker.js`: precache della shell, cache versionata `tassi-shell-v1.59.4`.
- Il service worker si registra solo su contesto sicuro (HTTPS o localhost), vedi `pwa.js:79`.

### Accesso

- Selezione dell'operatore con PIN di 6 cifre (`/api/auth/switch-operator`).
- Il login con password esiste ancora come rotta (`/api/auth/login`).
- Sessione su MariaDB (`express-mysql-session`).

### Docker

- `docker/docker-compose.yml`: servizi `db` e `app`, healthcheck, rotazione dei log, `container_name` parametrizzabile.
- Override: `docker-compose.nas-storage.yml` (uploads su NAS) e `docker-compose.local-test.yml` (ormai vuoto).
- `entrypoint.sh`: attende il DB, esegue `migrate:latest`, esegue il seed solo se `SEED_ON_START=true` e non siamo in produzione.

### Script di esercizio

In `scripts/`: `backup.sh`, `restore.sh`, `controlla-backup.sh`, `revoca-accessi.sh`, `individua-installazione.sh`.

---

## D. Dipendenze

### Runtime

- **Richiesto:** Node `>=24.0.0` (engines). Produzione su `node:24-alpine`.
- **Usato per i test in questa baseline:** Node **v24.21.0** / npm **11.19.0**, nel container `node:24-alpine`.
- L'host ha Node v22.22.2 / npm 10.9.7. È stato usato **solo** per le prove browser e per un singolo test che richiede `docker compose`.
- Il frontend non ha dipendenze né passaggio di build.

### Dipendenze backend

Sono 17 dirette, tutte di produzione; non ci sono devDependencies. L'albero completo conta 388 righe in `npm ls --all`. `npm ci` riproduce esattamente il lockfile (file identico prima e dopo).

| Pacchetto | Installato | Ultima disponibile | Uso verificato |
|---|---|---|---|
| express | 4.22.3 | 5.2.1 (major) | 17 file |
| express-session | 1.19.0 | = | `config/session.js` |
| express-mysql-session | 3.0.3 | = | `config/session.js` |
| express-rate-limit | 7.5.1 | 8.7.0 (major) | `middleware/security.js` |
| csrf-csrf | 3.2.2 | 4.0.3 (major) | `middleware/security.js` |
| helmet | 7.2.0 | 8.3.0 (major) | `middleware/security.js` |
| cors | 2.8.6 | = | `app.js` |
| cookie-parser | 1.4.7 | = | `app.js` |
| compression | 1.8.2 | = | `app.js` |
| morgan | 1.12.1 | = | `app.js` |
| knex | 3.3.0 | = | `config/db.js`, `productionCheck.js` |
| mysql2 | 3.24.4 | = | driver usato da knex (`client: 'mysql2'`), più `mysql2/promise` nei test; override per express-mysql-session |
| bcryptjs | 2.4.3 | 3.0.3 (major) | PIN e password (5 file) |
| multer | 2.4.0 | = | upload |
| pdfkit | 0.15.2 | 0.20.2 | `services/pdf.js` |
| qrcode | 1.5.4 | = | `services/qrcode.js` |
| dotenv | 16.6.1 | 18.0.4 (major) | `config/env.js`, `knexfile.js` |

Valutazione:
- **Vulnerabilità note:** `npm audit` → **0 vulnerabilities**, rilevato il 29/09/2026.
- **Dipendenze inutilizzate:** nessuna. Tutte e 17 sono richiamate dal codice.
- **Dipendenze obsolete:** 7 pacchetti sono indietro. 6 lo sono di una versione major; pdfkit è ancora in 0.x. Nessuno risulta vulnerabile. Nessun aggiornamento è stato fatto, come richiesto.
- **Duplicati:** `npm find-dupes` segnala solo `mime-db` 1.52.0/1.54.0, una differenza transitiva e trascurabile.

---

## E. Stato repository

| Voce | Esito |
|---|---|
| Branch / commit dell'Helpdesk | **non disponibili**: la consegna non contiene `.git` (vedi B) |
| Repository di sessione | `qrrt-web`, pulito; l'unico file non tracciato è questo report |
| File generati per errore | nessuno: niente `node_modules`, `*.log`, `.DS_Store`, `__MACOSX`, `uploads/`, `backups/`, `*.bak` |
| File `.env` reali | **nessuno**. Ci sono solo `backend/.env.example`, `docker/.env.example` e `docker/.env.qnap.example`, con valori segnaposto o vuoti |
| Segreti | nessuna chiave privata, token API o password reale. `SEED_ADMIN_PASSWORD=CambiaMi!2026` è un segnaposto, ed è anche il valore di riserva in `env.js:171` |
| `.gitignore` | 🟢 esclude `docker/.env` ma **non `backend/.env`**, che è proprio il file caricato da `config/env.js`. `.dockerignore` invece lo esclude |
| Dati personali | 🟡 i test contengono anagrafiche che **sembrano reali**: ragioni sociali, indirizzi, cellulari ed email di attività di Tuoro sul Trasimeno e Castiglione del Lago (`tests/integration/lottoL.test.js:47-51`, `tests/browser/lottoL.browser.js:54-56`). Ci sono anche nomi di persone (`tests/browser/aiuti/serverFinto.js`). Non è stato verificato se i dati siano davvero reali |
| Percorsi personali | solo nel `.sha256` della consegna (`/Users/daniele/Desktop/...`), non nel codice |

---

## F. Database

- **DBMS:** MariaDB 10.11, con driver `mysql2` tramite knex 3.3.
- **Migrazioni:** 51 file in `backend/src/db/migrations/`, dal `20260101000001_create_users` al `20260923000001_create_acceptance_sequences`.
  - Creano 36 tabelle applicative.
  - La tabella `sessions` è creata da express-mysql-session.
  - Tutte le migrazioni hanno una `down()`, ma alcune perdono dati; per esempio `semplifica_stati_ticket` non può ricostruire gli stati originali.
- **Esecuzione verificata:** `migrate:latest` da zero sul DB di test, senza errori (suite `migrations.test.js`: nessuna migrazione pendente).
- **Schema di riferimento:** 🟢 `database/schema-reference.sql` (33 tabelle) **non è allineato** alle migrazioni:
  - mancano `trusted_devices`, `ticket_technicians`, `ticket_activities` e `notification_preferences`;
  - mancano colonne come `users.pin_hash` e `tecnico_assegnabile`, `tickets.apparecchiatura_modello/matricola`, `customers.referente/provincia`;
  - `acceptance_statuses.colore` risulta `VARCHAR(20)` invece di 40.

  Il README lo dichiara solo documento di riferimento, ma è fuorviante.
- **Inizializzazione:** `entrypoint.sh` → `migrate:latest`. Seed demo solo se `SEED_ON_START=true` e `NODE_ENV≠production`.
- **Seed:** i 9 file chiamano tutti `assertSeedAllowed()`. Questa funzione blocca solo `NODE_ENV === 'production'` (`seedGuard.js`). Il seed `02_users` cancella gli utenti e crea utenti demo con password note.
- **Transazioni:** le operazioni critiche usano transazioni e `FOR UPDATE`: accettazioni (creazione, consegna, eliminazione), operatori, numerazione pratiche, gruppi, allegati.
  - Senza transazione: creazione e modifica degli interventi, generazione del report PDF dell'intervento, rigenerazione del token QR, eliminazione dei clienti.
  - Nell'eliminazione dei ticket il controllo sta fuori dalla transazione (BL-05).
- **Numerazione:**
  - ticket: MAX+1 con ritentativo sul vincolo UNIQUE (`ticketNumber.js`, `utils/numerazioneConcorrente.js`);
  - pratiche: tabella `acceptance_sequences` con `ON DUPLICATE KEY` + `FOR UPDATE`, monotona anche dopo le eliminazioni.
- **Backup** (`scripts/backup.sh`):
  - `mariadb-dump --single-transaction` e `tar` degli uploads;
  - copia di `docker/.env` e `backend/.env`;
  - manifest SHA-256, controlli di integrità (`gzip -t`, `-- Dump completed`, numero di `CREATE TABLE`);
  - rinomina atomica, retention a 14 giorni, `umask 077`.
- **Restore** (`scripts/restore.sh`):
  - verifica del manifest e delle impronte, poi conferma `CONFERMO`;
  - **backup di sicurezza preventivo**;
  - stop dell'app, DROP di tutte le tabelle e import con rollback automatico al backup di sicurezza se qualcosa fallisce;
  - uploads sostituiti con un container `--network none`;
  - verifica finale con `/api/health`.
- **Nessuna operazione di backup o ripristino è stata eseguita su dati reali in questa fase.** Gli script sono stati esercitati solo dalla suite `backupRestore.test.js`, che usa un "docker finto". La prova DR descritta in `docs/PROVA-DISASTER-RECOVERY.md` non è stata ripetuta.

---

## G. Test disponibili

| Suite | Posizione | Numero | Requisiti | Nel comando `npm test`? |
|---|---|---|---|---|
| Unitari | `backend/tests/unit/*.test.js` | 30 file | nessuno; `backupRestore` usa `bash` e un docker finto; 1 test usa il vero `docker compose` | sì |
| Integrazione | `backend/tests/integration/*.test.js` | 40 file | MariaDB raggiungibile; DB `<nome>_test` creato in automatico, rifiuto se il nome non termina in `_test`; uploads in una cartella temporanea | sì |
| Browser | `backend/tests/browser/*.browser.js` | 18 script | Playwright + Chromium; server finto (`aiuti/serverFinto.js`), nessun DB | **no**, vanno lanciati a mano uno per uno |
| Prove macOS | `backend/tests/mac/*.sh` (+ `verificaSlaDatiReali.js`) | 12 file | stack Docker reale su Mac, con dati reali per lo SLA | no, **non eseguite** |

Dipendenze dall'ambiente:
- Il test `PP-10/PP-13/PP-25/PP-26 "docker compose config" reale` (`lottoF1.test.js:257`) si salta da solo se manca `docker compose`.
- Le prove browser, se `playwright` non è installato localmente, lo cercano in un percorso assoluto fisso: `require('/opt/node22/lib/node_modules/playwright')`.
- Il glob `tests/**/*.test.js` dipende dalla shell: in `sh`/`bash` senza globstar diventa `tests/*/*.test.js`. Oggi il risultato è corretto perché non ci sono sottocartelle più profonde.

---

## H. Risultati test

### Backend (`npm test`)

Eseguito in Node 24.21.0 (`node:24-alpine`) con MariaDB 10.11.19 isolata.

| Esecuzione | Totali | PASS | FAIL | SKIP | Durata |
|---|---|---|---|---|---|
| Solo unitari (`npm run test:unit`) | 415 | 414 | 0 | 1 | 10,1 s |
| Suite completa, 1ª | **748** | **747** | **0** | **1** | 3 min 56 s |
| Suite completa, 2ª | 748 | 747 | 0 | 1 | 3 min 59 s |
| Suite completa con copertura, 3ª | 748 | 747 | 0 | 1 | circa 4 min |

- **Test saltato:** `"docker compose config" reale`, perché nell'immagine `node:24-alpine` non c'è `docker compose`. È stato eseguito a parte sull'host (Node 22 + Docker Compose 5.1.1): `lottoF1.test.js` → **21/21 PASS, 0 skip**.
- **Totale effettivo: 748/748 superati**, di cui 1 in un ambiente diverso.
- **Flaky:** nessuno. Le tre esecuzioni complete hanno dato risultati identici.
- **Nota di trasparenza:** `report-v1.59.4.md` dichiara "0 saltati". Il dato è coerente solo in un ambiente con `docker compose` disponibile, quindi è dipendente dall'ambiente, non un errore.

### Browser (Playwright, Chromium)

Host Node 22.22.2; ogni script lanciato con `node tests/browser/<x>.browser.js`.

| Suite | Controlli OK | NON OK | Durata |
|---|---|---|---|
| bozzaRisposta | 22 | 0 | 32 s |
| lottoD | 64 | 0 | 200 s |
| lottoE | 80 | 0 | 59 s |
| lottoG | 74 | 0 | 58 s |
| lottoI | 12 | 0 | 6 s |
| lottoJ | 13 | 0 | 3 s |
| lottoK | 17 | 0 | 3 s |
| lottoL | 9 | 0 | 5 s |
| v1511 | 145 | 0 | 8 s |
| v152 | 108 | 0 | 63 s |
| v153 | 95 | 0 | 36 s |
| v154 | 55 | 0 | 11 s |
| v155 | 82 | 0 | 17 s |
| v156 | 132 | 0 | 24 s |
| v157 | 111 | 0 | 26 s |
| v158 | 61 | 0 | 47 s |
| v159 | 164 | 0 | 39 s |
| v1591 | 33 | 0 | 34 s |
| **Totale: 18 suite** | **1277** | **0** | **671 s** |

### Copertura del codice backend

Misurata con `--experimental-test-coverage` su `src/**`, in-process: **92,56% delle righe, 78,56% dei branch, 85,66% delle funzioni.**

Aree con copertura bassa, cioè **aree importanti poco coperte**:

| File | Righe | Funzioni |
|---|---|---|
| `controllers/categories.controller.js` | 42,9% | 0% |
| `controllers/notifications.controller.js` | 57,4% | 0% |
| `controllers/equipment.controller.js` | 60,4% | 40% |
| `controllers/acceptanceStatuses.controller.js` | 66,7% | — |
| `controllers/dashboard.controller.js` | — | 45% |
| `routes/filters.routes.js` (filtri salvati) | 70% | 0% |
| `middleware/auth.js` | 79,4% | — |
| `services/sessionRevocation.js` | — | branch 50% |
| `controllers/ticketMessages.controller.js` | — | branch 35,7% |
| provider demo (`DemoEquipmentProvider`, `EquipmentProvider`) | 48–73% | — |

Il 26,5% di `scripts/cliPrompt.js` e il 45% di `seedDemo.js` sono in parte esercitati in sottoprocessi, che la copertura in-process non misura.

**Non coperti da test automatici:**
- le prove `tests/mac/*.sh`;
- la prova DR reale;
- l'installazione su QNAP;
- il comportamento reale su iOS/Android della PWA (service worker attivo solo su HTTPS);
- la resa grafica dei PDF (i test controllano bytes e intestazione, non il layout).

---

## I. Superficie di attacco (mappatura, non audit)

### Catena globale dei middleware (`app.js`)

Ordine di esecuzione:
1. `trust proxy`, spento di default;
2. `helmet` (CSP con `script-src 'self' 'unsafe-inline'`, `frame-ancestors 'none'`);
3. `compression`, `morgan`;
4. **originPolicy** (Origin uguale a Host, oppure presente in `CORS_ORIGIN`; altrimenti 403);
5. `cors` (origine riflessa, credentials);
6. `express.json` (limite 2 MB), `cookieParser`, sessione;
7. su `/api`: `apiLimiter` (300/min per IP), `Cache-Control: no-store`, **CSRF** (double-submit, `csrf-csrf`) su tutto tranne `GET /api/csrf-token` e `POST /api/auth/login`.

### Endpoint pubblici (senza autenticazione)

| Endpoint | Protezione |
|---|---|
| `GET /api/csrf-token` | — |
| `GET /api/health` | espone `env` |
| `POST /api/auth/login` | esente da CSRF; `loginLimiter` 10 ogni 15 min per IP, 5 ogni 15 min per username |
| `POST /api/auth/logout` | — |
| `GET /api/auth/me` | — |
| `GET /api/auth/device-info` | — |
| `GET /api/auth/operators` | elenco pubblico di id, nome, cognome e ruolo |
| `POST /api/auth/switch-operator` | PIN; `pinSwitchLimiter` 20 ogni 15 min per IP+operatore |
| `GET /public-status/:token` | `qrPublicLimiter` 30/min; fuori da `/api` |
| file statici e catch-all verso `index.html` | — |

### Superfici principali

| Superficie | Dove | Note di baseline |
|---|---|---|
| Login con password | `auth.controller.js:36-99` | attivo, bcrypt, tempi uniformi, `session.regenerate`; il frontend non lo usa |
| PIN | `services/pinAuth.js` | 6 cifre, bcrypt costo 10; ritardo progressivo fino a 30 s, **nessun blocco definitivo**, nessun avviso |
| Sessioni | `config/session.js` | cookie `th_sid` httpOnly, `sameSite=lax`, `secure` = `COOKIE_SECURE` (default false), rolling; durata assoluta spenta (`SESSION_MAX_HOURS=0`); utente ricaricato dal DB a ogni richiesta |
| Cookie dispositivo | `services/deviceAuth.js` | `th_device` httpOnly, token di 32 byte; nel DB solo lo SHA-256 |
| CSRF | `middleware/security.js:377-394` | cookie `th_csrf` più header `x-csrf-token`, legato alla sessione |
| Cambio operatore | `js/operatorSwitch.js`, `auth.controller.js:205-278` | rigenera la sessione |
| Upload | `services/attachments.js`, `attachmentSniff.js` | multer in memoria, 5 file da 15 MB; whitelist di estensioni e MIME; magic bytes solo per jpg/png/gif/webp/pdf; nome su disco casuale; protezione dal path traversal |
| Download / allegati | `attachments.js:111-118,210-248` | `Content-Disposition: attachment`, nosniff; serve solo l'autenticazione, nessun controllo per record (scelta di prodotto) |
| PDF | `services/pdf.js` | pdfkit `doc.text()`, font WinAnsi |
| Firme | `services/signatureImage.js` | solo PNG, massimo 1,5 MB, decodifica con tetto sui pixel |
| QR / pagina pubblica | `acceptancePublicToken.js`, `services/publicStatus.js`, `public/status.html` | token di 30 byte; dati minimi; escape dell'output |
| Input utente, XSS | frontend (circa 250 `innerHTML`) | `escapeHtml` usato quasi ovunque; eccezioni in BL-06 |
| Ricerca / SQL | `search.controller.js`, tutti i `raw`/`whereRaw` | **tutti con binding o testo costante**; `%` e `_` non escapati |
| CSV | `utils/csv.js:109-131` | protezione dalle formule presente |
| Operazioni admin | `technicians`, `groups`, `settings/*`, `devices/revoke`, `DELETE tickets/customers/acceptances` | `requireRole('amministratore')`; protezione dell'ultimo amministratore |
| Eliminazioni | ticket, pratiche, clienti, attività, KB | fisiche; operatori e gruppi logiche |
| Credenziali dei clienti | `services/secureCredentials.js` | AES-256-GCM; chiave = SHA-256 del segreto, con ricaduta su `CSRF_SECRET` |
| Backup / restore | `scripts/*.sh` | eseguiti da shell sul NAS, non esposti via HTTP |
| Controllo all'avvio | `controlloAvvio.js`, `qualitaSegreti.js` | blocca segreti deboli in produzione; `DB_PASSWORD` non è controllata |

---

## J. Funzioni critiche

1. **Accesso:** PIN, cambio operatore, revoca delle sessioni (`pinAuth`, `auth.controller`, `sessionRevocation`, `middleware/auth.js`).
2. **Numerazione:** ticket (`ticketNumber.js`) e pratiche (`acceptanceNumber.js`, `acceptance_sequences`).
3. **Accettazione:**
   - creazione transazionale di pratica + ticket + token;
   - consegna con chiusura del ticket;
   - firma cliente;
   - ricevuta ed etichetta PDF.
4. **Eliminazioni:** pratiche (robusta), ticket (vedi BL-05), clienti, operatori (soft delete, ultimo amministratore protetto).
5. **SLA:** `sla.js`, `slaCalc.js`, `businessHours.js`.
6. **Allegati e firme:** scrittura "tutto o niente", verifica dei magic bytes, download.
7. **Credenziali dei dispositivi dei clienti:** cifratura, rivelazione con audit.
8. **Backup e ripristino:** `backup.sh`, `restore.sh`, `revoca-accessi.sh`.
9. **Avvio in produzione:** `controlloAvvio.js`, `productionCheck.js`, `entrypoint.sh` (migrazioni automatiche).

---

## K. Audit icone e asset grafici

### Sintesi

- **Libreria:** tutta l'interfaccia usa un'unica libreria SVG inline in stile Lucide, `frontend/js/icons.js`.
  - 88 icone in `ICON_PATHS`, generate da `icon()` (riga 118): `viewBox="0 0 24 24"`, `fill="none"`, `stroke="currentColor"`, `stroke-width="2"`, `aria-hidden="true"`, `focusable="false"`.
  - Circa 408 chiamate a `icon()`.
- **Assenze verificate:**
  - nessun font-icon, sprite o file `.svg`;
  - nessun `<svg>` letterale nelle pagine;
  - nessun PNG/JPG/WebP usato come icona;
  - nessun `data:image/png` o raster dentro SVG;
  - nessuna emoji o simbolo Unicode usato come icona a schermo.
- **Qualità dei tracciati:** nessuno script, event handler, `foreignObject`, `<metadata>`, attributo Inkscape/Sketch o commento dentro i tracciati.
- **Spessore:** `stroke-width` uniforme (2).
- **Accessibilità:** tutti i 35 pulsanti solo-icona controllati hanno `aria-label` e/o `title`. Le icone decorative hanno `aria-hidden`.

### Totali

| Voce | Numero |
|---|---|
| **Icone UI non SVG** | **0** |
| Emoji usate come icona a schermo | **0**. Le emoji restano solo come chiavi di conversione legacy: `icons.js:127-133`, `status.html:72-77`, migrazione `20260909000003:16-31` e la sua `down()` |
| Simboli Unicode usati come icona | **0**. `·`, `&middot;`, `&rarr;` e `──────` sono separatori o testo |
| SVG con raster incorporato | **0** |
| SVG anomali o duplicati | 1 registro duplicato (`public/status.html`, 18 icone, con `calendar` diverso e `clockAlert` mancante); 6 SVG come data URI nel CSS, con colori fissi |
| Asset inutilizzati | `img/logo-tassiufficio-orizzontale.png` (solo in precache); icone `chevronsLeft`, `chevronsRight`, `externalLink`; classe CSS `.success-tick` |

### Immagini legittime (non segnalate come errore)

- Loghi TASSIUFFICIO in `img/`.
- Icone PWA, favicon e apple-touch.
- 11 splash iOS, tutti referenziati.
- QR code generati.
- Firme e allegati degli utenti.

### ICON-AUDIT

| ID | Sev. | Schermata | Funzione | Implementazione attuale | Formato | Problema | File | Posizione | Correzione consigliata |
|---|---|---|---|---|---|---|---|---|---|
| ICO-01 | 🟠 | Scheda cliente, mobile ≤900px | Azioni rapide Nuovo ticket / Chiama / Email | `icon('ticket'/'phone'/'mail')` in `.mcd-qa-btn` | SVG currentColor | `background: var(--text); color:#fff`: in tema scuro `--text` = `#e3eaf3`, quindi icona bianca su fondo quasi bianco (circa 1,2:1). **Verificato** | `frontend/css/style.css`; `frontend/pages/customer-detail.html` | style.css:1243-1246 (tema scuro :4194); customer-detail.html:294-296 | `background: var(--primary)` oppure `color: var(--surface)` |
| ICO-02 | 🟡 | Elenco Ticket / Elenco Accettazioni | Interruttore vista schede / tabella | tickets: schede=`list`, tabella=`dashboard`; accettazioni: tabella=`list`, schede=`dashboard` | SVG | Significato delle icone **invertito** fra le due pagine. **Verificato** | `pages/tickets.html`; `pages/accettazioni.html` | tickets:142-143; accettazioni:88-89 | Uniformare (tabella=`list`, schede=`dashboard`) e aggiungere `aria-pressed` |
| ICO-03 | 🟡 | Pagina pubblica di stato (QR) | Icona dello stato pratica | Registro locale `STATUS_ICON_PATHS` | SVG inline | Manca `clockAlert`, e 🟠 è mappata su `clock` (in `icons.js` e nella migrazione è `clockAlert`): uno stato con icona `clockAlert` **non mostra alcuna icona** al cliente. **Verificato** | `frontend/public/status.html` | 51-70, 76, 81 | Aggiungere `clockAlert` e allineare la mappa legacy; meglio usare un'unica fonte |
| ICO-04 | 🟡 | Pagina pubblica di stato | Registro icone | Copia di 18 tracciati di `icons.js` | SVG inline duplicato | Duplicazione; `calendar` diverso (mancano i "puntini") | `frontend/public/status.html` | 51-70 (calendar :69) | Un file condiviso per le icone di stato, senza dipendenze |
| ICO-05 | 🟡 | Select (Nuovo ticket, filtri Ticket/Accettazioni, bottom sheet, dettaglio ticket, Nuova accettazione) | Freccia a tendina | `chevronDown` come SVG data URI, `stroke=#6b7280`, ripetuto 4 volte | SVG in `background-image` | Duplicato; colore fisso fuori dai token; contrasto circa 3:1 in tema scuro | `frontend/css/style.css` | 1790, 3946, 3974, 3997 | Una sola regola; `mask-image` + `background-color: var(--text-muted)` |
| ICO-06 | 🟡 | Campi autocomplete (cliente) | Lente | `::before` con SVG data URI `#6b7280`, `opacity .55` | SVG in background | Colore fisso; contrasto sotto 3:1 in tema scuro; duplica `search` | `frontend/css/style.css` | 488-500 (url :498) | `mask-image` + token; niente opacity |
| ICO-07 | 🟡 | Dashboard, desktop | Lente nella barra di ricerca | SVG data URI `stroke=#2670b8` | SVG in background | Colore fisso, diverso da ICO-06 per la stessa funzione | `frontend/css/style.css` | 1967 | Come ICO-06 |
| ICO-08 | 🟡 | Sidebar / bottom nav / login | "Dashboard" | sidebar `home`, bottom nav `chart`, login `chart` | SVG | Due icone diverse per la stessa voce | `js/common.js`; `pages/index.html` | common.js:9, 48; index.html:72 | Una sola icona |
| ICO-09 | 🟡 | Menu, FAB, Dashboard, Scheda cliente, Ticket | "Nuovo ticket" | `circlePlus` / `ticket` / `ticketPlus` / `plus` | SVG | 4 icone diverse per la stessa azione | common.js:11, 83; dashboard.html:55; customer-detail.html:126, 294; tickets.html:70 | vedi file | Standardizzare su `ticketPlus` |
| ICO-10 | 🟢 | Login, pannello blu | Voce "Ticket" | `headphones` | SVG | Diversa da `ticket`, usata ovunque altrove | `pages/index.html` | 69 | `ticket` |
| ICO-11 | 🟢 | Nuova accettazione | "Cambia cliente" | `pencil` | SVG | Unico `pencil`; tutte le altre "Modifica" usano `penSquare` | `pages/accettazione-nuova.html` | 116 | `penSquare` |
| ICO-12 | 🟡 | Modali, banner, KB, mostra PIN, campanella, hamburger, notifiche, etichette | Chiudi / menu / toggle | `.nc-x` circa 28px, `.kbm-x` circa 26px, `.cst-banner-x`/`.kbp-banner-x` circa 24px, `.nc-eye` circa 28px, `.kbp-menu-btn` 34px, `.notif-bell` 38px, `.hamburger` 40px, `.nf-del` 34px, `.remove-tag` 28px | SVG | Area di tocco **sotto i 44px** su mobile; la regola a 44px copre solo `.icon-btn` e `.btn.icon-only` | `frontend/css/style.css` | 106 (regola 44px); 2992, 2848, 2598-2601, 2756, 3057-3060, 2808-2811, 612-619, 586-597, 709-716 | Estendere la media query ≤900px a queste classi |
| ICO-13 | 🟢 | Tutti i pulsanti solo-icona | Stato di focus | Outline predefinito del browser; `:focus-visible` dedicato solo per `.mw-close`, `.sb-toggle`, `[data-tooltip]` | CSS | Focus non uniforme; `.view-toggle button` senza `:hover` | `frontend/css/style.css` | 100-101, 119, 841, 1523-1527, 4112, 4609 | Regola `:focus-visible` comune |
| ICO-14 | 🟡 | Impostazioni → Stati pratica (API) | Colonna `icona` | Il backend accetta qualsiasi stringa, emoji comprese | Dato DB | Nessuna whitelist: un nome inesistente produce "nessuna icona" in silenzio. **Verificato** | `backend/src/controllers/acceptanceStatuses.controller.js` | 15-25, 33-43 | Validare contro i nomi di `STATUS_ICON_CHOICES` |
| ICO-15 | ℹ️ | Migrazione stati pratica | Rollback | `down()` riconverte i nomi in emoji | Dato DB | Un rollback reintrodurrebbe emoji | `migrations/20260909000003_acceptance_statuses_icone_svg.js` | 58-67 | `down()` senza effetto sulla colonna icona |
| ICO-16 | ℹ️ | Compatibilità legacy | Mappe emoji → icona | 3 mappe diverse (`icons.js`, `status.html`, migrazione) | JS | 🟠 va in `clockAlert` o in `clock`; `icons.js` non normalizza il selettore di variante U+FE0F | `js/icons.js`; `public/status.html`; migrazione | icons.js:127-139; status.html:72-81; migr.:16-31 | Una sola mappa; normalizzare U+FE0F |
| ICO-17 | ℹ️ | Registro icone | Icone non usate | `chevronsLeft`, `chevronsRight`, `externalLink` | SVG | Definite, mai referenziate | `js/icons.js` | 64, 65, 73 | Rimuovere o documentare |
| ICO-18 | ℹ️ | PWA | Logo orizzontale | PNG 54 KB | PNG, legittimo | Mai mostrato: solo in precache, quindi scaricato inutilmente | `frontend/service-worker.js` | 53 | Toglierlo dalla precache |
| ICO-19 | ℹ️ | Login | Logo simbolo | PNG 877×1200 (44 KB) mostrato a 86px | PNG, legittimo | Solo peso | `pages/index.html`; `css/style.css` | index:48-49; css:3611 | Variante ridotta |
| ICO-20 | ℹ️ | Pagina pubblica di stato | Favicon | Nessun `<link rel="icon">` | — | `/favicon.ico` finisce nel catch-all, che risponde con `index.html`: richiesta inutile | `public/status.html` | head | Aggiungere `<link rel="icon">` |
| ICO-21 | ℹ️ | CSS | Classe morta | `.success-tick` | CSS | Non usata | `css/style.css` | 130-131 | Rimuovere |
| ICO-22 | ℹ️ | Tutte | Scala delle dimensioni | Circa 30 dimensioni diverse (12–28px, 0,85–2em) | CSS | Nessuna scala a token | `css/style.css` | es. 186, 626, 694, 1110, 1996, 3318, 4122 | Token `--icon-sm/md/lg` |
| ICO-23 | ℹ️ | Documentazione | README | "timeline ed emoji" | Testo | Descrizione superata | `README.md` | 5 | Aggiornare |
| ICO-24 | ℹ️ | PDF | Font | Helvetica (WinAnsi); nessun simbolo nel codice | Testo PDF | Emoji inserite dagli utenti nei campi liberi verrebbero rese male | `backend/src/services/pdf.js` | 37-38, 55-75, 166-177 | Facoltativo: filtrare i caratteri fuori da WinAnsi |
| ICO-25 | ℹ️ | Manifest PWA | Icone delle scorciatoie | Le 3 scorciatoie usano tutte `icon-192.png` | PNG, legittimo | Nessuna distinzione visiva | `frontend/manifest.json` | 28, 34, 40 | Facoltativo |

**Riepilogo ICON-AUDIT:** 🔴 0 · 🟠 1 · 🟡 10 · 🟢 3 · ℹ️ 11. Totale: 25 voci.

Nessuna voce riguarda icone raster, emoji o simboli usati come icona. Sono tutte questioni di coerenza, tema scuro, duplicazione, accessibilità touch o pulizia.

---

## L. Problemi già evidenti

Sono stati trovati durante la mappatura, **senza** l'audit approfondito. La colonna "Verifica" dice come ogni punto è stato controllato.

### 🔴 CRITICO

Nessuno.

### 🟠 ALTO

| ID | File / posizione | Descrizione | Impatto | Evidenza | Verifica |
|---|---|---|---|---|---|
| BL-01 | `backend/src/services/pinAuth.js:28,115,136`; `routes/auth.routes.js:34`; `middleware/security.js` (pinSwitchLimiter) | L'unico fattore d'accesso quotidiano è un PIN di 6 cifre. Ritardo massimo 30 s, **nessun blocco definitivo**, nessun avviso all'amministratore. L'elenco degli operatori, ruolo compreso, è pubblico | Brute force in LAN su più operatori in parallelo. Stima teorica: circa 2.880 tentativi al giorno per operatore, cioè circa 44% di trovare almeno un PIN su 10 operatori in 30 giorni. Gli amministratori sono identificabili | `const PIN_FORMAT = /^\d{6}$/;` · `const DELAY_MAX_MS = 30000;` · `router.get('/operators', authController.operatorsPublic);` | Lettura del codice e calcolo; **non misurato** |
| BL-02 | Consegna `tassiufficio-helpdesk-v1.59.4.zip` | Nessun repository `.git` consegnato; il repository della sessione è un'altra app (QR RT) | La baseline non è riconducibile a un commit o tag: non si possono fare diff affidabili con la v1.59.3 né verificare la catena delle modifiche | `find . -name ".git*"` → solo `.gitignore`; `git log` di qrrt-web = 3 commit di QR RT | Ispezione diretta |

### 🟡 MEDIO

| ID | File / posizione | Descrizione | Impatto | Evidenza | Verifica |
|---|---|---|---|---|---|
| BL-03 | `scripts/createAdmin.js:40`; `auth.controller.js:36-99`; `app.js:126-129` | Il login con password è ancora attivo, esente da CSRF, e `create-admin` imposta una password reale. `CODICE-MORTO-MAPPA.md` sottostima la cosa | Secondo canale d'accesso per il primo amministratore, fuori dal ritardo del PIN | `ask('Password (min. 10 caratteri): ')` | Lettura del codice |
| BL-04 | `docker/docker-compose.yml:81`, file `.env*.example` | `COOKIE_SECURE=false` e HTTP in chiaro di default | PIN, cookie di sessione e credenziali dei dispositivi viaggiano in chiaro in LAN/Wi-Fi | `COOKIE_SECURE=false` | Lettura del codice |
| BL-05 | `backend/src/controllers/tickets.controller.js:916-934`; `services/ticketNumber.js:24-29` | Il controllo "ticket vuoto" sta **fuori** dalla transazione e senza `FOR UPDATE`; la numerazione è MAX+1 | Un allegato o intervento creato nella finestra fra controllo ed eliminazione viene cancellato a cascata (file orfano). Il numero dell'ultimo ticket eliminato viene riassegnato | `const c = await contenutoTicket(...)` poi `db.transaction(... delete())` | Lettura del codice |
| BL-06 | `frontend/js/common.js:1806-1811`; `frontend/pages/settings.html:516`; `acceptanceStatuses.controller.js:33-43` | `stato_colore` interpolato **senza escape** in `class="badge ${cls}"`; `s.codice` senza escape in `data-codice`; il backend non valida `colore` | XSS persistente da input dell'amministratore, eseguita nel browser di tutti gli operatori (la CSP ammette `unsafe-inline`) | `` return `<span class="badge ${cls}">…` `` | Lettura del codice; **non eseguito** |
| BL-07 | `backend/src/controllers/interventions.controller.js:206-207` | Firma dell'intervento salvata con un nome fisso `firma-cliente.png` | Una nuova firma sovrascrive la precedente senza evento né audit | `path.join(dir, 'firma-cliente.png'); fs.writeFileSync(...)` | Lettura del codice |
| BL-08 | `backend/src/controllers/ticketActivities.controller.js:63-92` | Qualsiasi operatore modifica o elimina attività altrui; l'audit salva solo l'`activityId` | Storico alterabile senza traccia del testo precedente | `logAction(..., { activityId: existing.id })` | Lettura del codice |
| BL-09 | `scripts/backup.sh:380-382` | Il backup copia `docker/.env` e `backend/.env`, con i segreti, accanto al dump che contiene `credenziali_enc`; il backup non è cifrato | Chi ottiene una copia del backup decifra le password dei dispositivi dei clienti | `cp "$ENV_FILE" "$WORK/config/docker.env.bak"` | Lettura del codice |
| BL-10 | `backend/tests/integration/lottoL.test.js:47-51`; `tests/browser/lottoL.browser.js:54-56` | Anagrafiche con ragioni sociali, indirizzi, cellulari ed email che sembrano reali | Tema GDPR se il codice viene condiviso | righe citate | Lettura; **realtà dei dati non verificata** |
| BL-11 | `backend/src/config/env.js:78,95`; `middleware/auth.js` | Nessuna durata massima della sessione (`SESSION_MAX_HOURS=0`) e polling che rinnova | Una scheda aperta su una postazione condivisa resta autenticata a tempo indeterminato | default `0` / `false` | Lettura del codice (scelta documentata) |
| BL-12 | `backend/Dockerfile` | Nessuna istruzione `USER`: Node gira come root nel container | Maggiore impatto di un'eventuale RCE o di una scrittura su file | `grep USER` → nessun risultato | Lettura diretta |

### 🟢 BASSO

| ID | File / posizione | Descrizione | Verifica |
|---|---|---|---|
| BL-13 | `routes/interventions.routes.js:14`; `interventions.controller.js:246-299` | `GET …/report.pdf` (senza ruolo, senza CSRF) scrive un file e righe nel DB, fuori da transazione | Lettura |
| BL-14 | `interventions.controller.js:87-108,155-164` | Creazione e modifica degli interventi con scritture multiple senza transazione | Lettura |
| BL-15 | `services/acceptancePublicToken.js:213-227` | Revoca e creazione del token QR non atomiche: con richieste concorrenti possono restare due token attivi | Lettura |
| BL-16 | `backend/src/db/seedGuard.js` | Blocca solo `NODE_ENV==='production'`: fuori da Docker, con `NODE_ENV` non impostato, `knex seed:run` cancella gli utenti | Lettura |
| BL-17 | `.gitignore` | Non esclude `backend/.env` | Lettura diretta |
| BL-18 | `database/schema-reference.sql` | Disallineato dalle migrazioni: 4 tabelle e diverse colonne mancanti, `colore` a 20 invece di 40 | `grep` diretto |
| BL-19 | `services/secureCredentials.js`; `config/env.js:186` | Chiave AES = SHA-256 del segreto, con ricaduta su `CSRF_SECRET` se `ACCEPTANCE_CREDENTIALS_SECRET` manca | Lettura |
| BL-20 | `services/signatureImage.js`; `services/attachments.js:55-69` | Upload e firme bufferizzati in memoria (fino a circa 75 MB per richiesta): DoS limitato, solo da utenti autenticati | Lettura |
| BL-21 | `acceptances.controller.js:341-347,938-939` | File di firma scritti dentro la transazione: se la transazione viene annullata restano orfani | Lettura |
| BL-22 | `scripts/restore.sh:323` | Rifiuta percorsi assoluti e `..` nell'archivio, ma non i symlink | Lettura |
| BL-23 | `controllers/groups.controller.js:124` | Un body malformato svuota i membri del gruppo (già noto in `CODICE-MORTO-MAPPA.md`) | Lettura |
| BL-24 | `tests/browser/*.browser.js`; `docs/TESTING.md` | Le prove browser cercano Playwright in un percorso assoluto fisso `/opt/node22/...`; la documentazione dice "Node 20.6+" contro `engines >=24` | Lettura ed esecuzione |

### ℹ️ INFORMATIVO

| ID | File / posizione | Nota |
|---|---|---|
| BL-25 | `app.js:126-129` | Login esente da CSRF: login CSRF teoricamente possibile |
| BL-26 | `app.js:152-158` | `/api/health` pubblico espone `env` (`production`/`test`) |
| BL-27 | `auth.controller.js:223-236` | I codici 404/409/401 distinguono "operatore inattivo", "senza PIN" e "PIN errato" |
| BL-28 | `scripts/backup.sh:343` | Password del DB passata come argomento a `mariadb-dump`, nel container |
| BL-29 | `middleware/security.js:245-247`; `routes/publicStatus.routes.js:1-3` | Commenti non aggiornati |
| BL-30 | `technicians.controller.js:166-172` | `update` accetta `ruolo` senza whitelist applicativa (vincolato dall'enum del DB) e una `password` che riattiva il login con password |
| BL-31 | `search.controller.js` | `LIKE` senza escape di `%` e `_`: solo un tema di prestazioni o precisione |
| BL-32 | `backend/package.json` | 7 dipendenze indietro, di cui 6 di una major (express 5, helmet 8, csrf-csrf 4, …); 0 vulnerabilità note |
| BL-33 | `report-v1.59.4.md` §B | Dichiara 0 test saltati: vero solo con `docker compose` disponibile |
| BL-34 | `README.md:5` | Stato di progetto ("FASE 2") e riferimento alle emoji non aggiornati |
| BL-35 | `scripts/backup.sh` | Dump del DB e archivio degli uploads presi in momenti diversi ad applicazione attiva: coerenza fra i due non garantita |

### Conteggio problemi (BL + ICO)

| Severità | BL | ICO | Totale |
|---|---|---|---|
| 🔴 CRITICO | 0 | 0 | **0** |
| 🟠 ALTO | 2 | 1 | **3** |
| 🟡 MEDIO | 10 | 10 | **20** |
| 🟢 BASSO | 12 | 3 | **15** |
| ℹ️ INFORMATIVO | 11 | 11 | **22** |

---

## M. Aree che richiedono audit approfondito

1. **Autenticazione PIN:** brute force misurato e test di carico sul limiter; valutare un blocco o un avviso all'amministratore; enumerazione degli operatori; DNS rebinding sull'originPolicy (ipotesi).
2. **XSS:** revisione sistematica dei circa 250 `innerHTML`, con attenzione ai campi amministrativi (`stato_colore`, `codice`) e ai valori in attributi.
3. **Integrità transazionale:** eliminazione dei ticket, interventi e firme, token QR, file scritti dentro le transazioni.
4. **Backup e restore:** ripetere la prova DR in un ambiente isolato; cifratura dei backup; separazione dei segreti dal dump; symlink in restore.
5. **Trasporto:** HTTPS e `COOKIE_SECURE` sull'installazione reale (QNAP); PWA con service worker attivo.
6. **Upload e download:** tipi senza magic bytes (docx, xlsx, txt, csv); limiti di memoria; controllo per record, se richiesto dal dominio.
7. **Docker hardening:** utente non root, `read_only`, porte, rete; esecuzione di `production-check` sull'installazione reale.
8. **Aree poco coperte dai test:** notifiche, categorie, apparecchiature, filtri salvati, dashboard, revoca delle sessioni.
9. **Dati personali nei test** e politica di condivisione del codice.
10. **Icone:** ICO-01 (tema scuro), ICO-02/03 (coerenza e pagina pubblica), ICO-12 (aree di tocco).
11. **Tracciabilità:** consegna del repository git o di un tag verificabile della v1.59.4.

---

## Appendice — ambiente e comandi usati

- **Copia di lavoro:** estrazione dello zip in scratchpad, duplicata in `run/` per i test. L'originale estratto non è stato toccato.
- **DB:**
  ```
  docker run -d --name th-test-db -e MARIADB_ROOT_PASSWORD=… -p 127.0.0.1:33306:3306 mariadb:10.11
  ```
  Versione 10.11.19. I test creano `tassiufficio_helpdesk_test`.
- **Test backend:**
  ```
  docker run --rm --network host -e DB_HOST=127.0.0.1 -e DB_PORT=33306 … node:24-alpine sh -c "npm ci; npm test"
  ```
- **Dipendenze:** `npm ci`, `npm audit`, `npm outdated`, `npm ls`, `npm find-dupes`, tutti nel container `node:24-alpine`.
- **Browser:** `node tests/browser/<suite>.browser.js`, Playwright + Chromium dell'host.
- **Copertura:**
  ```
  node --test --test-concurrency=1 --experimental-test-coverage --test-coverage-include='src/**'
  ```
- **Nessun file del progetto modificato, nessun aggiornamento, nessuna operazione su dati reali.**
