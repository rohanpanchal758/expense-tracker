# Personal Expense Tracker

A simple Python + SQLite expense tracker with a Streamlit web interface.

## Features
- Add, view, and delete expenses
- Store records persistently in SQLite
- Summarize total spending and current-month spending
- Visualize spending by category
- Export expense records to CSV
- Use parameterized SQL statements for database operations

## Tech stack
Python · Streamlit · SQLite · SQL · Pandas

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
The app creates `expenses.db` automatically in the project folder.

## SQL concepts demonstrated
- `CREATE TABLE`
- `INSERT`
- `SELECT`
- `DELETE`
- `GROUP BY`
- `SUM`
- Parameterized queries

## Future improvements
Add budgets, recurring expenses, monthly comparisons, user accounts, and unit tests.

## Portfolio description
Built a personal expense tracker using Python, Streamlit, and SQLite, with CRUD operations, SQL-based spending summaries, category visualizations, and CSV export.
