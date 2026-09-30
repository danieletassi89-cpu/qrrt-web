# Modello dati preliminare — Verifiche fiscali

> **Schema preliminare, nessuna modifica al database reale.**
> Lo stack e lo schema reale di TASSIUFFICIO Helpdesk non sono disponibili in questa sessione: i nomi delle tabelle esistenti sono **segnaposto** (`hd_*`) da sostituire con quelli veri. SQL scritto in forma neutra (compatibile PostgreSQL/MySQL con piccoli adattamenti).

## 1. Mappa: riuso vs nuove tabelle

| Concetto | Tabella | Stato | Note |
|---|---|---|---|
| Cliente | `hd_customers` | **Riuso** Helpdesk | Nessun campo fiscale aggiunto (P.IVA/CF già presenti ⚪) |
| Sede / punto vendita | `hd_customer_sites` | **Riuso** se esiste, altrimenti **nuova tabella Helpdesk** | Serve anche a ticket e agenda |
| Contatti | `hd_contacts` | Riuso | Per firmatario e invio email |
| Utenti / tecnici | `hd_users` | Riuso | |
| Apparecchiature cliente | `hd_assets` | **Riuso** se esiste, altrimenti **nuova tabella Helpdesk** generica | Un RT è un'apparecchiatura: compare nei ticket |
| Ticket / accettazioni | `hd_tickets`, `hd_intakes` | Riuso + colonna `asset_id` se manca | |
| Appuntamenti | `hd_appointments` | Riuso + `type` + tabella ponte | |
| Allegati | `hd_attachments` | Riuso + `sha256`, `immutable` | |
| Audit | `hd_audit_events` | Riuso se esiste, altrimenti **nuova, comune a tutto l'Helpdesk** | |
| Produttori / modelli | `device_manufacturers`, `device_models` | **Nuove**, generiche | Riusabili per POS/stampanti |
| Dettaglio RT | `fiscal_rt_devices` | **Nuova** | 1:1 con `hd_assets` |
| Storico installazioni RT | `fiscal_rt_placements` | **Nuova** | Trasferimenti cliente/sede |
| Laboratorio | `fiscal_lab_settings` | **Nuova** (riga unica) | |
| Profilo tecnico fiscale | `fiscal_technician_profiles` | **Nuova** | 1:1 con `hd_users` (storicizzabile) |
| Verifiche | `fiscal_checks` | **Nuova** | |
| Modelli checklist | `fiscal_checklist_templates`, `fiscal_checklist_template_items` | **Nuove** | Versionati |
| Risposte checklist | `fiscal_check_answers` | **Nuova** | |
| Firme | `fiscal_check_signatures` | **Nuova** | |
| Documenti della verifica | `fiscal_check_documents` | **Nuova** (ponte verso `hd_attachments`) | |
| Rettifiche | `fiscal_check_revisions` | **Nuova** | Snapshot versione precedente |
| Collegamento appuntamenti | `fiscal_check_appointments` | **Nuova** ponte | |
| Import | `import_batches`, `import_rows` | **Nuove** | Tracciabilità e annullamento import |

**Tabelle nuove del modulo: 16** (di cui 2 generiche riusabili: produttori/modelli; 2 tecniche per l'import). Più, solo se l'Helpdesk non le ha già: sedi, apparecchiature, audit.

## 2. Diagramma relazioni

```
hd_customers 1──< hd_customer_sites 1──< hd_assets 1──1 fiscal_rt_devices
                                            │  │               │
                         hd_tickets >───────┘  │               ├──< fiscal_rt_placements (storico cliente/sede)
                         hd_intakes >──────────┘               │
                                                               └──< fiscal_checks >── fiscal_checklist_templates ──< …_items
device_manufacturers 1──< device_models 1──< hd_assets                │
hd_users 1──1 fiscal_technician_profiles                               ├──< fiscal_check_answers >── template_items
hd_users 1──< fiscal_checks (technician_user_id)                       ├──< fiscal_check_signatures
hd_appointments >──< fiscal_checks (fiscal_check_appointments)         ├──< fiscal_check_documents >── hd_attachments
                                                                       └──< fiscal_check_revisions
hd_audit_events (entity_type, entity_id) ← tutte
```

## 3. Estensioni a tabelle Helpdesk (solo se mancano)

```sql
-- Sedi/punti vendita (se l'Helpdesk non le ha)
CREATE TABLE hd_customer_sites (
  id              BIGINT PRIMARY KEY,
  customer_id     BIGINT NOT NULL REFERENCES hd_customers(id),
  name            VARCHAR(120) NOT NULL,        -- insegna
  address         VARCHAR(160), zip VARCHAR(5), city VARCHAR(80), province CHAR(2),
  istat_code      CHAR(6),                      -- per filtri per zona
  phone           VARCHAR(40), notes TEXT,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL
);

-- Apparecchiature (se l'Helpdesk non le ha)
CREATE TABLE hd_assets (
  id              BIGINT PRIMARY KEY,
  customer_id     BIGINT NOT NULL REFERENCES hd_customers(id),
  site_id         BIGINT NULL REFERENCES hd_customer_sites(id),
  category        VARCHAR(20) NOT NULL,         -- 'RT','POS','PRINTER',...
  model_id        BIGINT NULL REFERENCES device_models(id),
  serial_number   VARCHAR(40),
  public_token    CHAR(26) UNIQUE,              -- per etichetta QR TASSIUFFICIO (non indovinabile)
  notes TEXT, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL
);

-- Collegamenti
ALTER TABLE hd_tickets       ADD COLUMN asset_id BIGINT NULL REFERENCES hd_assets(id);
ALTER TABLE hd_intakes       ADD COLUMN asset_id BIGINT NULL REFERENCES hd_assets(id);
ALTER TABLE hd_appointments  ADD COLUMN type VARCHAR(20) NOT NULL DEFAULT 'GENERIC'; -- 'FISCAL_CHECK'
ALTER TABLE hd_attachments   ADD COLUMN sha256 CHAR(64) NULL, ADD COLUMN immutable BOOLEAN NOT NULL DEFAULT FALSE;
```

## 4. Nuove tabelle

```sql
CREATE TABLE device_manufacturers (
  id BIGINT PRIMARY KEY, name VARCHAR(80) NOT NULL UNIQUE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE device_models (
  id BIGINT PRIMARY KEY,
  manufacturer_id BIGINT NOT NULL REFERENCES device_manufacturers(id),
  name VARCHAR(80) NOT NULL,
  category VARCHAR(20) NOT NULL,                -- 'RT','SERVER_RT','MF','POS',...
  approval_ref VARCHAR(60) NULL,                -- estremi approvazione modello ⚪
  is_portable BOOLEAN NOT NULL DEFAULT FALSE,   -- ambulante: attiva voci checklist dedicate
  checklist_template_id BIGINT NULL,            -- checklist predefinita
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  UNIQUE (manufacturer_id, name)
);

CREATE TABLE fiscal_rt_devices (
  asset_id BIGINT PRIMARY KEY REFERENCES hd_assets(id),
  device_kind VARCHAR(12) NOT NULL,             -- 'RT','SERVER_RT','MF'
  fiscal_serial VARCHAR(20) NOT NULL,           -- matricola RT (11) / 'logotipo+matricola' per MF storici
  status VARCHAR(16) NOT NULL,                  -- IN_MAGAZZINO, ATTIVO, FUORI_SERVIZIO, DISMESSO
  activated_on DATE NULL, decommissioned_on DATE NULL,
  warranty_until DATE NULL,
  contract_type VARCHAR(16) NULL,               -- SINGOLO, NOLEGGIO, CONTRATTO
  default_price DECIMAL(10,2) NULL,
  qr_payload TEXT NULL,                         -- payload QR AdE letto (così com'è)
  last_valid_check_id BIGINT NULL,              -- denormalizzati, aggiornati in transazione
  last_check_date DATE NULL,
  next_due_date DATE NULL,
  due_override_reason TEXT NULL,                -- solo correzione motivata/import
  legacy_ref VARCHAR(40) NULL,                  -- id vecchio sistema
  UNIQUE (device_kind, fiscal_serial)
);
CREATE INDEX ix_rt_due ON fiscal_rt_devices(status, next_due_date);

CREATE TABLE fiscal_rt_placements (             -- storico: dove/di chi era l'RT
  id BIGINT PRIMARY KEY,
  asset_id BIGINT NOT NULL REFERENCES fiscal_rt_devices(asset_id),
  customer_id BIGINT NOT NULL, site_id BIGINT NULL,
  from_date DATE NOT NULL, to_date DATE NULL,
  reason VARCHAR(40) NOT NULL                   -- INSTALLAZIONE, TRASFERIMENTO, RIENTRO
);

CREATE TABLE fiscal_lab_settings (              -- riga unica
  id SMALLINT PRIMARY KEY CHECK (id = 1),
  legal_name VARCHAR(120) NOT NULL, vat_number VARCHAR(16), tax_code VARCHAR(16),
  address VARCHAR(160), zip VARCHAR(5), city VARCHAR(80), province CHAR(2),
  email VARCHAR(120), phone VARCHAR(40),
  authorization_type VARCHAR(30),               -- 'LABORATORIO','FABBRICANTE'
  seal_prefix VARCHAR(30),                      -- identificativo alfabetico sigillo
  periodicity_months SMALLINT NOT NULL DEFAULT 24,
  due_rule VARCHAR(20) NOT NULL DEFAULT 'SAME_DAY', -- 'SAME_DAY' | 'END_OF_MONTH' ⚪
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE fiscal_technician_profiles (
  id BIGINT PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES hd_users(id),
  tax_code VARCHAR(16) NOT NULL,
  seal_alpha VARCHAR(30), seal_number INT,      -- punzone/sigillo personale
  is_lab_manager BOOLEAN NOT NULL DEFAULT FALSE,
  valid_from DATE NOT NULL, valid_to DATE NULL, -- periodo di abilitazione/collaborazione
  signature_image_attachment_id BIGINT NULL     -- firma tecnico precaricata (opzionale)
);

CREATE TABLE fiscal_checklist_templates (
  id BIGINT PRIMARY KEY,
  code VARCHAR(40) NOT NULL, version INT NOT NULL,
  title VARCHAR(120) NOT NULL, applies_to VARCHAR(12) NOT NULL, -- 'RT','MF'
  status VARCHAR(10) NOT NULL,                  -- BOZZA, ATTIVO, RITIRATO (un attivo non si modifica)
  UNIQUE (code, version)
);

CREATE TABLE fiscal_checklist_template_items (
  id BIGINT PRIMARY KEY,
  template_id BIGINT NOT NULL REFERENCES fiscal_checklist_templates(id),
  section_code VARCHAR(4) NOT NULL, section_title VARCHAR(120) NOT NULL,
  item_code VARCHAR(8) NOT NULL, text VARCHAR(400) NOT NULL,
  answer_type VARCHAR(10) NOT NULL,             -- OK_KO_NA, TEXT, NUMBER
  is_blocking BOOLEAN NOT NULL DEFAULT TRUE,    -- KO => esito negativo proposto
  photo_on_ko BOOLEAN NOT NULL DEFAULT FALSE,
  only_portable BOOLEAN NOT NULL DEFAULT FALSE,
  sort_order INT NOT NULL,
  UNIQUE (template_id, item_code)
);

CREATE TABLE fiscal_checks (
  id BIGINT PRIMARY KEY,
  number VARCHAR(20) UNIQUE,                    -- es. VF-2026-000123, assegnato alla chiusura
  asset_id BIGINT NOT NULL REFERENCES fiscal_rt_devices(asset_id),
  customer_id BIGINT NOT NULL, site_id BIGINT NULL,
  check_type VARCHAR(16) NOT NULL,              -- ATTIVAZIONE, PERIODICA, STRAORDINARIA, DISMISSIONE
  status VARCHAR(14) NOT NULL,                  -- PIANIFICATA, IN_CORSO, DA_FIRMARE, CONCLUSA, RETTIFICATA, ANNULLATA
  technician_user_id BIGINT NULL REFERENCES hd_users(id),
  technician_profile_id BIGINT NULL REFERENCES fiscal_technician_profiles(id),
  checklist_template_id BIGINT NULL REFERENCES fiscal_checklist_templates(id),
  planned_for TIMESTAMP NULL, started_at TIMESTAMP NULL, completed_at TIMESTAMP NULL,
  outcome VARCHAR(10) NULL,                     -- POSITIVO, NEGATIVO
  seal_found VARCHAR(12) NULL,                  -- INTEGRO, ASSENTE, MANOMESSO
  seal_applied VARCHAR(40) NULL,
  notes TEXT NULL,
  next_due_date DATE NULL,                      -- calcolata alla chiusura
  amount DECIMAL(10,2) NULL, is_paid BOOLEAN NOT NULL DEFAULT FALSE,
  billing_status VARCHAR(12) NOT NULL DEFAULT 'DA_FATTURARE', -- DA_FATTURARE, FATTURATO, NON_FATTURABILE, OMAGGIO
  billing_ref VARCHAR(40) NULL,
  ade_registered_at TIMESTAMP NULL, ade_reference VARCHAR(80) NULL,
  snapshot JSON NULL,                           -- cliente/sede/RT/tecnico/laboratorio al momento della chiusura
  source VARCHAR(12) NOT NULL DEFAULT 'APP',    -- APP, RAPIDA (da carta), IMPORT
  legacy_ref VARCHAR(40) NULL,
  cancel_reason TEXT NULL,
  created_by BIGINT NOT NULL, created_at TIMESTAMP NOT NULL, updated_at TIMESTAMP NOT NULL
);
CREATE INDEX ix_checks_asset ON fiscal_checks(asset_id, completed_at);
CREATE INDEX ix_checks_status ON fiscal_checks(status, planned_for);

CREATE TABLE fiscal_check_answers (
  id BIGINT PRIMARY KEY,
  check_id BIGINT NOT NULL REFERENCES fiscal_checks(id),
  template_item_id BIGINT NOT NULL REFERENCES fiscal_checklist_template_items(id),
  answer VARCHAR(4) NULL,                       -- OK, KO, NA
  value_text TEXT NULL,
  photo_attachment_id BIGINT NULL,
  answered_at TIMESTAMP NOT NULL, answered_by BIGINT NOT NULL,
  UNIQUE (check_id, template_item_id)
);

CREATE TABLE fiscal_check_signatures (
  id BIGINT PRIMARY KEY,
  check_id BIGINT NOT NULL REFERENCES fiscal_checks(id),
  role VARCHAR(10) NOT NULL,                    -- TECNICO, CLIENTE
  signer_name VARCHAR(120) NOT NULL,
  signer_contact_id BIGINT NULL,
  image_attachment_id BIGINT NULL,              -- NULL se CLIENTE_ASSENTE
  absent_reason TEXT NULL,
  signed_at TIMESTAMP NOT NULL, collected_by BIGINT NOT NULL,
  document_sha256 CHAR(64) NOT NULL,            -- hash del contenuto firmato
  UNIQUE (check_id, role)
);

CREATE TABLE fiscal_check_documents (
  id BIGINT PRIMARY KEY,
  check_id BIGINT NOT NULL REFERENCES fiscal_checks(id),
  attachment_id BIGINT NOT NULL REFERENCES hd_attachments(id),
  doc_type VARCHAR(20) NOT NULL,                -- RAPPORTO, DICHIARAZIONE, FOTO, RICEVUTA_ADE, IMPORTATO
  revision_no INT NOT NULL DEFAULT 1,
  sha256 CHAR(64) NOT NULL,
  generated_at TIMESTAMP NOT NULL,
  sent_to VARCHAR(200) NULL, sent_at TIMESTAMP NULL
);

CREATE TABLE fiscal_check_revisions (
  id BIGINT PRIMARY KEY,
  check_id BIGINT NOT NULL REFERENCES fiscal_checks(id),
  revision_no INT NOT NULL,
  reason TEXT NOT NULL,
  previous_snapshot JSON NOT NULL,              -- verifica + risposte + firme prima della rettifica
  created_by BIGINT NOT NULL, created_at TIMESTAMP NOT NULL,
  UNIQUE (check_id, revision_no)
);

CREATE TABLE fiscal_check_appointments (
  check_id BIGINT NOT NULL REFERENCES fiscal_checks(id),
  appointment_id BIGINT NOT NULL REFERENCES hd_appointments(id),
  PRIMARY KEY (check_id, appointment_id)
);

CREATE TABLE hd_audit_events (                  -- se non esiste già
  id BIGINT PRIMARY KEY,
  occurred_at TIMESTAMP NOT NULL,
  user_id BIGINT NULL, ip VARCHAR(45) NULL, user_agent VARCHAR(200) NULL,
  entity_type VARCHAR(40) NOT NULL, entity_id BIGINT NOT NULL,
  action VARCHAR(30) NOT NULL,                  -- CREATE, UPDATE, STATUS, SIGN, CLOSE, REVISE, CANCEL, EXPORT, IMPORT, DOWNLOAD
  before_data JSON NULL, after_data JSON NULL,
  request_id VARCHAR(40) NULL
);
CREATE INDEX ix_audit_entity ON hd_audit_events(entity_type, entity_id, occurred_at);

CREATE TABLE import_batches (
  id BIGINT PRIMARY KEY, source VARCHAR(20) NOT NULL, -- VF_MDB, VF_TXT_ADE, FW21_XLSX, ...
  file_name VARCHAR(200), file_sha256 CHAR(64),
  status VARCHAR(12) NOT NULL,                  -- ANALIZZATO, CONFERMATO, ANNULLATO
  stats JSON NULL, created_by BIGINT NOT NULL, created_at TIMESTAMP NOT NULL
);
CREATE TABLE import_rows (
  id BIGINT PRIMARY KEY, batch_id BIGINT NOT NULL REFERENCES import_batches(id),
  entity_type VARCHAR(30) NOT NULL, legacy_key VARCHAR(80) NOT NULL,
  raw JSON NOT NULL, action VARCHAR(12) NOT NULL, -- CREA, COLLEGA, AGGIORNA, SCARTA, DA_VERIFICARE
  target_id BIGINT NULL, message TEXT NULL
);
```

## 5. Regole di integrità

1. **Immutabilità** — `fiscal_checks` con `status IN ('CONCLUSA','RETTIFICATA','ANNULLATA')`: nessun `UPDATE` su campi tecnici né su risposte/firme. Doppia difesa: controllo nel servizio applicativo **e** trigger DB che rifiuta la modifica (eccezione: `ade_registered_at`, `ade_reference`, `billing_status`, `billing_ref`, `is_paid`, tracciate in audit). Nessun `DELETE` fisico: solo annullamento.
2. **Rettifica** — transazione: salva snapshot in `fiscal_check_revisions` → sblocca → modifica → rigenera PDF (nuova `revision_no`) → ricalcola scadenza RT → audit.
3. **Chiusura** — transazione unica: controlli (checklist completa, esito, firma tecnico, tecnico abilitato alla data) → numero verbale → snapshot → PDF + hash → `CONCLUSA` → aggiornamento `fiscal_rt_devices.last_*`/`next_due_date` → chiusura appuntamento → audit. Se un passo fallisce, rollback completo.
4. **Matricola** unica per tipo dispositivo; formato validato lato server.
5. **Un solo** `fiscal_checks` non concluso per RT alla volta (evita doppie verifiche aperte).
6. `fiscal_rt_devices.next_due_date` **derivato**: ricalcolabile in qualsiasi momento dall'ultima verifica valida (job di controllo notturno che segnala divergenze).
7. Chiavi esterne reali ovunque (contrario del vecchio programma).

## 6. Corrispondenza con il vecchio programma

| Vecchio (`dbvf.mdb`) | Nuovo |
|---|---|
| `clforn` (Azienda.mdb) | `hd_customers` (+ `hd_contacts` per persona di riferimento) |
| `ecr.ub_*` | `hd_customer_sites` (deduplicate per cliente+indirizzo) |
| `ecr` | `hd_assets` + `fiscal_rt_devices` (`device_kind='MF'`, `fiscal_serial = logotipo+matricola`) |
| `ecr.idcliente` / "installazione ad altro cliente" | `fiscal_rt_placements` |
| `ecr.data_defisc` | `status='DISMESSO'`, `decommissioned_on` |
| `ecr.sospeso` / `no_scad` | `status='FUORI_SERVIZIO'` / `DISMESSO` |
| `ecr.max_azz`, `n_azzeraenti` | `snapshot` delle verifiche MF importate (non più campi attivi) |
| `ecr.tipo`, `prezzo`, `scad_gar` | `contract_type`, `default_price`, `warranty_until` |
| `marchio`, `modello` | `device_manufacturers`, `device_models` (`category='MF'`) |
| `tecnico_incaricato` | `fiscal_technician_profiles` (+ utente Helpdesk disattivo se il tecnico non c'è più) — **password `pw_web` non migrata** |
| `soggetto_obbligato` | `fiscal_lab_settings` |
| `visure` | `fiscal_checks` (`source='IMPORT'`, `status='CONCLUSA'`, `snapshot` con i dati copiati) |
| `visure.tipoint` | `check_type` (MESSA IN SERVIZIO→ATTIVAZIONE, VERIFICA PERIODICA→PERIODICA, DEFISCALIZZAZIONE→DISMISSIONE, "entrambe"→ATTIVAZIONE) |
| `visure.esito` | `outcome` |
| `visure.importo`, `pagato`, `fatturato`, `idfatt` | `amount`, `is_paid`, `billing_status`, `billing_ref` |
