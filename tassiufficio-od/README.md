# tassiufficio-od

Verifica di fattibilità: catalogo OD+ → portale TASSIUFFICIO con ricarichi e raccolta ordini.

## Struttura

- `report/report.md`: report di verifica (bozza, da completare con le verifiche sul portale)
- `importatore/importa.py`: prototipo di normalizzazione e ricarichi (solo libreria standard; `openpyxl` per i file Excel)
- `config/mappatura_colonne.json`: collega le colonne dell'export OD+ ai campi normalizzati
- `config/ricarichi.csv`: regole di ricarico (`default`, `categoria`, `articolo`, `cliente_articolo`)
- `dati/originali/`: esportazioni scaricate a mano (escluse da git)

## Uso

```
python3 importatore/importa.py dati/originali/listino.csv --confronto
python3 importatore/importa.py dati/originali/listino.csv --cliente C001
```

Nessuna credenziale nel codice. Se in futuro servissero, vanno in `.env` (già in `.gitignore`).
