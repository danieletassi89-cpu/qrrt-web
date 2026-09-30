# Confronto: VerificheFiscali (Windows) · FiscalWeb21 · proposta TASSIUFFICIO

> **Versione preliminare.** La colonna *Vecchio Windows* è verificata sui file (vedi `ANALISI-VECCHIO-VERIFICHE-FISCALI.md`).
> La colonna *FiscalWeb21* è **attesa (⚪)**: il sito non era raggiungibile da questa sessione. Sarà corretta dopo la navigazione guidata.
> La colonna *Helpdesk* indica cosa **presumibilmente** esiste già in TASSIUFFICIO Helpdesk: il codice dell'Helpdesk non è in questa sessione, quindi va confermato.

**Classificazione:** `MANTENERE` · `MIGLIORARE` · `SEMPLIFICARE` · `ELIMINARE` · `NUOVA`
**Utilità:** ★★★ indispensabile · ★★ utile · ★ marginale

## 1. Anagrafiche

| Funzione | Vecchio Windows | FiscalWeb21 (⚪ atteso) | Utilità | Proposta TASSIUFFICIO | Classe |
|---|---|---|---|---|---|
| Anagrafica cliente | Tabella clienti del gestionale Magis, separata dall'assistenza | Propria anagrafica | ★★★ | **Un solo cliente**, quello dell'Helpdesk. Nessuna anagrafica fiscale separata | MIGLIORARE |
| Controllo duplicati cliente | Solo in import (per P.IVA) | ⚪ | ★★★ | Avviso in inserimento su P.IVA/CF uguali o nome simile | MIGLIORARE |
| Punto vendita | ❌ Indirizzo copiato dentro ogni apparecchio | ⚪ entità separata | ★★★ | Entità **Sede/Punto vendita** del cliente, condivisa con ticket e appuntamenti | NUOVA (rispetto al vecchio) |
| Persona di riferimento | 1 nome/cognome sul cliente | ⚪ | ★★ | Contatti multipli per cliente/sede (se già presenti nell'Helpdesk, riusarli) | MANTENERE |
| Laboratorio ("soggetto obbligato") | Scheda completa con sigillo e tipo abilitazione | ⚪ | ★★★ | Impostazioni modulo: dati laboratorio, abilitazione, identificativo sigillo | MANTENERE |
| Tecnici con sigillo e periodo collaborazione | Sì (CF, titolo, responsabile, sigillo alfa/num, date) | ⚪ | ★★★ | **Profilo tecnico fiscale** agganciato all'utente Helpdesk (non un'anagrafica a parte) | MIGLIORARE |
| Titolo di studio del tecnico | Sì | ⚪ | ★ | Solo se richiesto da documenti ufficiali | SEMPLIFICARE |
| Marchi e modelli | Tabelle semplici marca/modello | ⚪ | ★★ | Catalogo **produttori → modelli** con tipo (RT, server RT, ambulante), riusabile per altre apparecchiature | MIGLIORARE |

## 2. Apparecchi (RT)

| Funzione | Vecchio Windows | FiscalWeb21 (⚪) | Utilità | Proposta TASSIUFFICIO | Classe |
|---|---|---|---|---|---|
| Identificazione | Logotipo (2) + matricola (9), solo MF | ⚪ matricola RT | ★★★ | Matricola RT (11 caratteri) **validata e univoca**; campi MF solo per lo storico importato | MIGLIORARE |
| Legame apparecchio‑cliente | `idcliente` + copia nome | ⚪ | ★★★ | Apparecchio → **sede** → cliente, con storico delle installazioni | MIGLIORARE |
| Installazione ad altro cliente | Sì, operazione dedicata | ⚪ | ★★ | "**Trasferisci**" con storico (chi aveva l'RT e quando) | MANTENERE |
| Stati apparecchio | Attivo / sospeso / defiscalizzato (derivati da campi) | ⚪ | ★★★ | Stato esplicito: *in magazzino, attivo, fuori servizio, dismesso* | MIGLIORARE |
| Tipo contratto (singolo/noleggio/contratto) | Sì | ⚪ | ★★ | Mantenere, collegato al listino/contratto del cliente se l'Helpdesk lo gestisce | MANTENERE |
| Ultimo prezzo pagato | Sì | ⚪ | ★★ | Mostrato come informazione, ricavato dall'ultima verifica | SEMPLIFICARE |
| Garanzia | Data scadenza garanzia + filtro | ⚪ | ★★ | Mantenere | MANTENERE |
| Azzeramenti / esaurimento memoria | Sì (filtro "30 rimanenti") | — | ★ (solo MF) | Non applicabile agli RT: solo in storico | ELIMINARE |
| "Non mostrare nello scadenziario" | Flag | ⚪ | ★★ | Sostituito da **stato** (dismesso/fuori servizio escono da soli) + motivo | SEMPLIFICARE |
| Note | Nota apparecchio + nota cliente | ⚪ | ★★ | Note con autore e data | MIGLIORARE |
| QR code | ❌ | ⚪ | ★★★ | Lettura del **QR RT** e **etichetta QR TASSIUFFICIO** (l'app QR RT esiste già) | NUOVA |
| Foto apparecchio/targhetta | ❌ | ⚪ | ★★ | Foto da smartphone in fase di censimento/verifica | NUOVA |

## 3. Verifiche

| Funzione | Vecchio Windows | FiscalWeb21 (⚪) | Utilità | Proposta TASSIUFFICIO | Classe |
|---|---|---|---|---|---|
| Tipi intervento | Messa in servizio, verifica periodica, entrambe, defiscalizzazione | ⚪ | ★★★ | Tipi RT (attivazione/prima verifica, verificazione periodica, intervento su sigillo, dismissione) — **elenco da confermare** | MIGLIORARE |
| Avvio verifica dallo scadenziario | **Clic destro → Inserisci verifica** | ⚪ | ★★★ | Pulsante "**Avvia verifica**" su ogni riga in scadenza e nella scheda RT | MANTENERE |
| Dati precompilati | Sì (copiati dall'apparecchio) | ⚪ | ★★★ | Precompilazione totale; il tecnico conferma solo ciò che cambia | MANTENERE |
| Checklist | ❌ Solo stampa cartacea A1–F2 | ⚪ digitale | ★★★ | **Checklist digitale guidata**, versionata, esito per voce, note/foto sulle voci KO | NUOVA |
| Esito | Positivo/negativo manuale | ⚪ | ★★★ | Proposto automaticamente dalla checklist, confermato dal tecnico | MIGLIORARE |
| Stato sigillo / targhetta | Solo sul modulo cartaceo | ⚪ | ★★★ | Campi strutturati (sigillo trovato/applicato, identificativo) | NUOVA |
| Date inizio/fine | Sì | ⚪ | ★★ | Automatiche (avvio/chiusura), correggibili | SEMPLIFICARE |
| Calcolo prossima scadenza | Automatico al salvataggio | ⚪ | ★★★ | Automatico, **regola configurabile** (biennale RT), visibile prima della conferma | MANTENERE |
| Modifica verifica conclusa | Libera, anche eliminazione | ⚪ | ★★★ | **Bloccata**: solo *rettifica* motivata con nuova versione e audit | MIGLIORARE |
| Stato verifica | ❌ (record salvato = fatto) | ⚪ | ★★★ | Pianificata → In corso → Da firmare → Conclusa (→ Rettificata / Annullata) | NUOVA |
| Importo, pagato, fatturato | Sì | ⚪ | ★★ | Mantenere; "fatturato" collegato al sistema di fatturazione usato oggi | MANTENERE |
| Crea fattura dalla verifica | Sì (gestionale Magis) | ⚪ | ★★ | **Da decidere**: esportazione verso il gestionale di fatturazione, non una fatturazione nuova | SEMPLIFICARE |
| Durata intervento | Sul modulo cartaceo | ⚪ | ★ | Calcolata da avvio/chiusura | SEMPLIFICARE |

## 4. Documenti e firme

| Funzione | Vecchio Windows | FiscalWeb21 (⚪) | Utilità | Proposta TASSIUFFICIO | Classe |
|---|---|---|---|---|---|
| Rapporto/verbale di verifica | Checklist cartacea stampata precompilata | ⚪ PDF | ★★★ | **PDF generato dal sistema** con checklist compilata, esito, sigillo, firme | MIGLIORARE |
| Dichiarazione messa in servizio / dismissione | Sì | ⚪ | ★★ | Modelli equivalenti RT, se ancora richiesti (**da confermare**) | MIGLIORARE |
| Firma tecnico e cliente | A penna | ⚪ su schermo | ★★★ | Firma su schermo (dito/penna) + nome del firmatario, **hash del PDF** | NUOVA |
| Archiviazione | ❌ manuale | ⚪ | ★★★ | Automatica su verifica, RT e cliente, **immutabile** | NUOVA |
| Invio al cliente | ❌ | ⚪ email | ★★ | Email con PDF, registro invii; invio solo su conferma | NUOVA |
| Tagliandi/etichette | Stampa tagliandi | ⚪ | ★★ | **Etichetta QR** sull'RT con prossima scadenza (stampante BIXOLON già in uso) | MIGLIORARE |
| Elenchi stampabili | Elenco MF, elenco verifiche | ⚪ | ★★ | Export PDF/Excel dagli elenchi filtrati | MANTENERE |
| Editor dei modelli di stampa | Designer FastReport integrato | ⚪ | ★ | Modelli fissi versionati (modifica solo da sviluppo) | ELIMINARE |

## 5. Pianificazione

| Funzione | Vecchio Windows | FiscalWeb21 (⚪) | Utilità | Proposta TASSIUFFICIO | Classe |
|---|---|---|---|---|---|
| Scadenziario | Calendario + griglia, filtri località/prov./cliente | ⚪ | ★★★ | Dashboard con fasce (scadute, 7, 30, 60/90 gg) + **filtro per zona** | MIGLIORARE |
| Filtro per zona | Località, provincia | ⚪ | ★★★ | Mantenere, più ordinamento per comune per organizzare i giri | MANTENERE |
| Agenda appuntamenti | ❌ (solo calendario delle scadenze) | ⚪ | ★★★ | **Agenda unica Helpdesk** con tipo appuntamento "Verifica fiscale" | NUOVA |
| Assegnazione tecnico | Solo in fase di registrazione | ⚪ | ★★ | In pianificazione (appuntamento) | NUOVA |
| Promemoria al cliente | ❌ | ⚪ | ★★ | Avviso di scadenza/appuntamento via email (opzionale, su conferma) | NUOVA |

## 6. Rapporti con l'Agenzia delle Entrate

| Funzione | Vecchio Windows | FiscalWeb21 (⚪) | Utilità | Proposta TASSIUFFICIO | Classe |
|---|---|---|---|---|---|
| File trimestrale verifiche (MF) | Sì (tracciato 13635/2010) | — | — (non più applicabile agli RT) | Solo **lettura** dei vecchi file per migrazione | ELIMINARE |
| Registrazione esito RT sul portale AdE | — | ⚪ da capire | ★★★ | Fase 1: **promemoria + campo "registrato su AdE il…"** con ricevuta allegata. Integrazione automatica solo se esistono servizi ufficiali utilizzabili | NUOVA |
| Link al libretto elettronico (QR) | — | ⚪ | ★★ | Salvare l'URL del QR RT e aprirlo dalla scheda | NUOVA |

## 7. Piattaforma

| Funzione | Vecchio Windows | FiscalWeb21 (⚪) | Utilità | Proposta TASSIUFFICIO | Classe |
|---|---|---|---|---|---|
| Accesso | PC singolo | Web | ★★★ | Web/PWA Helpdesk | MIGLIORARE |
| Mobile | App Android + sync FTP manuale | ⚪ web responsive | ★★★ | **Stessa PWA** su iPhone/Android/tablet, dati in tempo reale | MIGLIORARE |
| Offline | App mobile (probabilmente) | ⚪ | ★★ | Bozza della verifica salvata sul dispositivo se manca rete, invio alla riconnessione (lotto successivo) | NUOVA |
| Ruoli e permessi | ❌ | ⚪ | ★★★ | Ruoli Helpdesk + permessi fiscali specifici | NUOVA |
| Audit log | ❌ | ⚪ | ★★★ | Completo, non modificabile | NUOVA |
| Backup | Copia manuale `.mdb` | ⚪ gestito dal fornitore | ★★★ | Backup automatici DB + allegati, prova di ripristino | MIGLIORARE |
| Import dati | Da file trimestrali AdE | ⚪ | ★★★ | Import guidato con anteprima, deduplica e annullamento | MIGLIORARE |
| Aggiornamenti/licenza | Controllo online, attivazione | Cloud | — | Non pertinente (software proprio) | ELIMINARE |

## 8. Legame assistenza ↔ fiscale

| Funzione | Vecchio Windows | FiscalWeb21 (⚪) | Utilità | Proposta TASSIUFFICIO | Classe |
|---|---|---|---|---|---|
| Da apparecchio a scheda riparazione | Sì (crea scheda riparazione dal MF) | ⚪ probabilmente assente | ★★★ | Dalla scheda RT: **apri ticket/accettazione** già collegati all'RT | MIGLIORARE |
| Da ticket a verifica | ❌ | ⚪ | ★★★ | Se il ticket riguarda un RT con verifica scaduta/in scadenza → **avviso** e proposta di verifica nello stesso intervento | NUOVA |
| Esito negativo → riparazione | ❌ | ⚪ | ★★★ | Esito negativo crea (su conferma) un **ticket** precompilato | NUOVA |
| Storico unico dell'apparecchio | Separato (verifiche vs riparazioni) | ⚪ | ★★★ | **Timeline unica** dell'RT: installazione, verifiche, ticket, trasferimenti, documenti | NUOVA |

---

## 9. Dove il vecchio programma è più veloce

1. **Scadenziario = schermata iniziale**: nessun passaggio per vedere cosa c'è da fare.
2. **Da riga in scadenza a verifica in un clic**, con tutto precompilato.
3. **Una sola maschera** per la verifica (niente procedure a più pagine): quando la checklist è cartacea, registrare l'esito richiede ~30 secondi.
4. **Filtri a caselle** immediati (sospesi, dismessi, in garanzia).

➜ Il nuovo modulo deve **mantenere questa rapidità** anche aggiungendo checklist e firme: la checklist va resa veloce (tutto "OK" con un tocco, si toccano solo le eccezioni), e deve esistere una **"registrazione rapida"** per inserire verifiche già fatte su carta (utile anche nel periodo di transizione).

## 10. Sintesi

| Classe | Numero funzioni | Esempi |
|---|---|---|
| MANTENERE | 11 | scadenziario per zona, avvio verifica dalla riga, calcolo scadenza, trasferimento RT |
| MIGLIORARE | 20 | cliente unico, stato RT, checklist→esito, PDF, mobile, import |
| SEMPLIFICARE | 6 | flag scadenziario, fatturazione, date/durata automatiche |
| ELIMINARE | 4 | azzeramenti MF, file trimestrale, editor stampe, licenze |
| NUOVA | 20 | checklist digitale, firma, archivio immutabile, agenda unica, QR, audit, legame ticket |

*(Conteggi indicativi; verranno ricalcolati dopo l'analisi di FiscalWeb21.)*
