# Analisi di FiscalWeb21 (cloud.fiscalweb21.it)

> **Stato: DA COMPLETARE durante la navigazione guidata con te.**
> In questa sessione il sito `cloud.fiscalweb21.it` (e anche il portale dell'Agenzia delle Entrate) **non è raggiungibile**: la rete della sandbox blocca la connessione (errore 403 del proxy). Non ho quindi visto FiscalWeb21 e **nulla di quanto segue è un'osservazione diretta**.
>
> Questo documento serve a:
> 1. fissare **il metodo** con cui analizzeremo FiscalWeb21 insieme;
> 2. preparare **la griglia** da compilare sezione per sezione;
> 3. elencare le **domande** a cui la navigazione deve rispondere, già orientate al confronto col vecchio programma e al progetto TASSIUFFICIO.

## Legenda

| Simbolo | Significato |
|---|---|
| ✅ OSSERVATO | Visto durante la navigazione guidata (screenshot o descrizione tua). |
| 🟡 DEDOTTO | Ricavato da ciò che si vede (es. un campo implica una logica). |
| ⚪ ATTESO | Ipotesi a priori, da confermare o smentire. |

---

## 1. Regole della navigazione

- **Sola lettura.** Nessuna creazione, modifica, cancellazione, firma, invio email/PEC, comunicazione all'Agenzia o import reale senza tua autorizzazione esplicita.
- Se una funzione è interessante ma "scrive" (es. *Nuova verifica*), la analizziamo **fino al pulsante di conferma** e poi annulliamo, oppure usiamo un record di prova che mi indichi tu.
- Nessuna copia di codice, testi, grafica o icone di FiscalWeb21: annoto **funzioni e flussi**, non l'aspetto.
- Dati personali dei tuoi clienti: negli appunti li sostituisco con segnaposto (`CLIENTE_A`, `RT_1`…).

### Come procedere in pratica

Dato che non posso aprire il sito da qui, la modalità più efficace è:

1. **Tu** apri una sezione e mi mandi **1–3 screenshot** (lista + dettaglio + eventuale maschera di inserimento), aggiungendo a voce cosa succede cliccando.
2. **Io** compilo la scheda della sezione (§3), segno ✅/🟡 e ti faccio le domande mirate.
3. Alla fine aggiorno `CONFRONTO-VERIFICHE-FISCALI.md` sostituendo le colonne "FiscalWeb21 (atteso)" con quanto osservato.

Ordine consigliato (dal più importante per il tuo lavoro quotidiano):

1. Dashboard → 2. Verifiche periodiche (elenco + nuova + dettaglio) → 3. Checklist → 4. Firma e PDF → 5. RT / matricole → 6. Clienti e punti vendita → 7. Scadenze e agenda → 8. Tecnici → 9. Modelli/produttori → 10. Ricerca, filtri, report → 11. Import/export → 12. Notifiche, mobile, QR, POS.

---

## 2. Contesto normativo di riferimento (da fonti pubbliche, da riverificare)

Da risultati di ricerca pubblici (non ho potuto aprire i documenti ufficiali):

- Gli **RT** sono soggetti a **verificazione periodica biennale**; la prima verificazione coincide con l'attivazione.
- La verificazione è eseguita da **laboratori/tecnici abilitati** iscritti presso l'Agenzia; il tecnico **registra l'esito** tramite la procedura dedicata del portale **"Fatture e Corrispettivi"**, applica il **sigillo**, e il **libretto** del dispositivo è elettronico, consultabile tramite il **QR code** dell'RT.
- In caso di esito negativo il dispositivo risulta non conforme e non utilizzabile fino a nuovo intervento.
- L'Agenzia pubblica un documento sulle **"prove minime"** che la verificazione deve contenere: è la base ideale per la **checklist RT** del nuovo modulo. ➜ *Serve che tu me ne fornisca copia (o la checklist che usa FiscalWeb21), perché da qui non posso scaricarlo.*

Fonti da consultare: [AdE – Laboratori e tecnici abilitati](https://www.agenziaentrate.gov.it/portale/it/misuratori-fiscali-e-registratori-telematici/laboratori-e-tecnici-abilitati-per-la-verifica-periodica-dei-misuratori-fiscali) · [AdE – Descrizione prove minime (PDF)](https://www.agenziaentrate.gov.it/portale/documents/20143/4972665/Descrizione+prove+minime_v1.pdf/5ea7a2e1-602b-1bcf-758a-12da4c470149) · [AdE – Chiarimenti su RT (PDF)](https://www.agenziaentrate.gov.it/portale/documents/20143/2340020/chiarimenti+e+precisazioni+registratore+cassa+rt_Chiarimenti+e+precisazioni+su+RT_aprile2109_def.pdf/4ad3a7cd-01f8-18e8-a87c-7a78046e435d) · [AdE – Procedura di controllo MF e RT](https://www.agenziaentrate.gov.it/portale/misuratori-fiscali-e-registratori-telematici/procedura-di-controllo-misuratori-fiscali-e-registratori-telematici)

**Domanda chiave per te:** oggi la registrazione dell'esito sul portale AdE la fai **a mano sul portale** o è **FiscalWeb21 a farla/prepararla**? Questo cambia molto il perimetro del nuovo modulo (vedi progetto, §"Rapporto con l'Agenzia").

---

## 3. Schede da compilare per sezione

Per ogni sezione: **scopo**, **elenco/colonne**, **campi del dettaglio**, **azioni**, **input → elaborazione → output**, **stati**, **pro/contro operativi**, **idea per TASSIUFFICIO**.

### 3.1 Dashboard
| Voce | Annotazioni |
|---|---|
| Riquadri/contatori | ⚪ scadute, in scadenza, fatte nel mese |
| Clic su un contatore → | ⚪ lista filtrata |
| Utilità reale per il tecnico | |
| Cosa manca / cosa è superfluo | |

### 3.2 Clienti
| Voce | Annotazioni |
|---|---|
| Campi anagrafici (P.IVA, CF, PEC, SDI…) | |
| Ricerca (per nome, P.IVA, matricola?) | |
| Scheda cliente: cosa mostra (punti vendita, RT, verifiche, documenti) | |
| Duplicati: controllo su P.IVA? | |

### 3.3 Punti vendita
| Voce | Annotazioni |
|---|---|
| Entità separata dal cliente? | ⚪ sì |
| Campi (insegna, indirizzo, referente, orari?) | |
| Relazione con RT (un RT → un punto vendita) | |
| Trasferimento RT tra punti vendita/clienti | |

### 3.4 Registratori telematici / matricole
| Voce | Annotazioni |
|---|---|
| Campi (matricola 11 caratteri, modello, produttore, data attivazione, stato, firmware?) | |
| Stati RT (attivo, in servizio, fuori servizio, dismesso…) | |
| Validazione formato matricola | |
| Storico interventi/verifiche sul singolo RT | |
| QR code: viene letto? generato? | |
| Collegamento al libretto elettronico AdE | |

### 3.5 Modelli e produttori
| Voce | Annotazioni |
|---|---|
| Anagrafica precaricata o manuale? | |
| Dati del modello (n. approvazione, tipo RT/server RT, ambulante?) | |

### 3.6 Tecnici
| Voce | Annotazioni |
|---|---|
| Dati (CF, abilitazione, sigillo/punzone, periodo) | |
| Accesso separato per tecnico / permessi | |
| Firma del tecnico memorizzata? | |

### 3.7 Verifiche periodiche — elenco e dettaglio
| Voce | Annotazioni |
|---|---|
| Colonne dell'elenco | |
| Stati della verifica (bozza, in corso, completata, firmata, inviata, annullata…) | |
| Tipi di intervento (verificazione periodica, attivazione, intervento tecnico, dismissione…) | |
| Campi del dettaglio | |
| Numerazione dei verbali | |
| Modificabilità dopo la chiusura | |

### 3.8 Inserimento / modifica verifica — flusso
Da ricostruire come:
```
[punto di partenza] → [scelta cliente/RT] → [dati intervento] → [checklist] → [esito] → [firma] → [documento] → [scadenza]
```
| Passo | Input | Elaborazione | Output | Click/tempo stimato |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

### 3.9 Checklist
| Voce | Annotazioni |
|---|---|
| Voci (testo, numerazione, gruppi) | |
| Esiti possibili per voce (OK/KO/N.A.) | |
| Note/foto per voce | |
| Checklist diverse per tipo intervento/modello? | |
| Voce KO → esito negativo automatico? | |

### 3.10 Firma
| Voce | Annotazioni |
|---|---|
| Firma grafometrica su schermo (tecnico/cliente) | |
| Firma remota (link al cliente)? | |
| Cosa viene firmato esattamente (PDF, dati) | |

### 3.11 Documenti, PDF, stampe, invio
| Voce | Annotazioni |
|---|---|
| Documenti generati (verbale, rapporto, checklist, ricevuta…) | |
| Dove sono archiviati, come si ritrovano | |
| Invio (email/PEC/WhatsApp), log invii | |
| Formato stampa (A4, termica) | |

### 3.12 Scadenze e agenda
| Voce | Annotazioni |
|---|---|
| Calcolo prossima scadenza (biennale da quale data?) | |
| Vista calendario (giorno/settimana/mese), per tecnico | |
| Programmazione e spostamento appuntamenti | |
| Promemoria al cliente (email/SMS) | |

### 3.13 Ricerca, filtri, storico, report
| Voce | Annotazioni |
|---|---|
| Ricerca globale | |
| Filtri disponibili | |
| Report (per periodo, per tecnico, fatturato…) | |
| Export (CSV/Excel/PDF) | |

### 3.14 Import / export
| Voce | Annotazioni |
|---|---|
| Esportazione **completa** dei dati (clienti, RT, verifiche, scadenze)? | **Fondamentale per la migrazione** |
| Formato (CSV, Excel, JSON, API) | |
| Esportazione dei PDF/documenti archiviati | |
| Import da altri software | |

### 3.15 Notifiche, mobile, QR, POS
| Voce | Annotazioni |
|---|---|
| Notifiche interne/push/email | |
| Uso da smartphone (responsive? app?) | |
| Lettura QR RT | |
| Gestione POS o altre apparecchiature | |

---

## 4. Aspettative da verificare (⚪)

Ipotesi che la navigazione deve confermare o smentire, utili al confronto:

1. Gestione **clienti → punti vendita → RT** come gerarchia.
2. **Checklist digitale** con esito per voce e **firma su schermo**.
3. **PDF del verbale** generato e archiviato automaticamente, con invio email.
4. **Scadenziario biennale** calcolato in automatico.
5. **Esportazione** dati in Excel/CSV (da verificare quanto completa).
6. Interfaccia utilizzabile da **tablet/smartphone** ma pensata per desktop.
7. **Nessun collegamento** con ticket/accettazioni di assistenza (è un gestionale verticale).

---

## 5. Output atteso a fine navigazione

- Questo documento completato con ✅/🟡 per ogni sezione.
- Mappa dei flussi reali (`input → elaborazione → output`).
- Elenco dei **dati esportabili** e del formato (per `MIGRAZIONE-DATI-VERIFICHE-FISCALI.md`).
- Aggiornamento della matrice in `CONFRONTO-VERIFICHE-FISCALI.md`.
