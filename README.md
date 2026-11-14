# RecallKit

<p align="center"><img src="assets/banner.svg" alt="RecallKit animated banner" width="100%"></p>

A private, local-first flashcard trainer using a lightweight SM-2-inspired spaced-repetition scheduler.

## Features
- Again / Hard / Good / Easy review grades
- Automatic due dates and ease adjustment
- SQLite database stored beside the script
- CSV import/export and due-card statistics
- No account, cloud sync or third-party packages

## Run
Python 3.9+:

```bash
python app.py add "HTTP 404" "The requested resource was not found."
python app.py study
python app.py stats
python app.py export cards.csv
python app.py import more-cards.csv
```

CSV files use `front` and `back` columns. Use `python app.py --help` for details.