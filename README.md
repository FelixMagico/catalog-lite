# Software Catalog

Sito Flask in cui gli utenti si registrano, guardano un catalogo di software e
chiedono di installarne uno; l'amministratore approva o rifiuta le richieste.

## Per provarlo rapidamente

Servono Python 3.11+, XAMPP con MySQL acceso e MySQL Workbench (o phpMyAdmin).

1. In Workbench: `CREATE DATABASE catalog_lite CHARACTER SET utf8mb4;`
2. Nella cartella del progetto:

   ```
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   playwright install chromium
   ```

3. Copiare `.env.example` in `.env` (di default funziona con XAMPP: utente `root`, senza password; in `SECRET_KEY` va scritta una stringa qualsiasi).
4. Creare tabelle e dati di esempio, poi avviare:

   ```
   flask db upgrade
   flask seed-db
   flask run
   ```

5. Aprire http://127.0.0.1:5000

| Ruolo | Username | Password |
| --- | --- | --- |
| Amministratore | `admin` | `admin123` |
| Utente | si crea da "Registrati" | a scelta (min. 6 caratteri) |

**Come si usa:** l'utente richiede un software dal catalogo (stato "In attesa");
l'admin, dalla pagina Admin, approva o rifiuta; l'utente vede il nuovo stato.
L'admin non vede il catalogo, solo le richieste.

## Test

```
pytest
```

5 test: 3 con Playwright e 2 sull'API. 
`pytest tests/test_ui.py --headed --slowmo 500`.

