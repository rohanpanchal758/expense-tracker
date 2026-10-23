import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).with_name("expenses.db")

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0)
            )
        """)

def load_expenses():
    with connect() as conn:
        return pd.read_sql_query(
            "SELECT id, expense_date, category, description, amount FROM expenses ORDER BY expense_date DESC, id DESC",
            conn
        )

init_db()
st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")
st.title("💸 Personal Expense Tracker")
st.caption("Track spending, manage records, and understand where your money goes.")

with st.sidebar:
    st.header("Add an expense")
    expense_date = st.date_input("Date", value=date.today())
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Education", "Health", "Entertainment", "Other"])
    description = st.text_input("Description", placeholder="e.g. Train ticket")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0, format="%.2f")
    if st.button("Add expense", type="primary", use_container_width=True):
        if not description.strip():
            st.error("Please add a short description.")
        elif amount <= 0:
            st.error("Amount must be greater than zero.")
        else:
            with connect() as conn:
                conn.execute(
                    "INSERT INTO expenses (expense_date, category, description, amount) VALUES (?, ?, ?, ?)",
                    (expense_date.isoformat(), category, description.strip(), amount)
                )
            st.success("Expense added.")
            st.rerun()

df = load_expenses()
if df.empty:
    st.info("No expenses yet. Add one using the sidebar to get started.")
else:
    total = float(df["amount"].sum())
    month_key = date.today().strftime("%Y-%m")
    this_month = float(df.loc[df["expense_date"].str.startswith(month_key), "amount"].sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("Total recorded spending", f"₹{total:,.2f}")
    c2.metric("Spending this month", f"₹{this_month:,.2f}")
    c3.metric("Number of expenses", f"{len(df)}")

    st.subheader("Spending by category")
    category_summary = df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
    st.bar_chart(category_summary.set_index("category"))

    st.subheader("Expense records")
    display_df = df.copy()
    display_df["amount"] = display_df["amount"].map(lambda x: f"₹{x:,.2f}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.subheader("Delete an expense")
    selected = st.selectbox(
        "Choose a record",
        options=df["id"].tolist(),
        format_func=lambda item: f"#{item} — {df.loc[df.id == item, 'description'].iloc[0]} (₹{df.loc[df.id == item, 'amount'].iloc[0]:,.2f})"
    )
    confirm = st.checkbox("I confirm I want to delete this record.")
    if st.button("Delete selected expense", disabled=not confirm):
        with connect() as conn:
            conn.execute("DELETE FROM expenses WHERE id = ?", (int(selected),))
        st.success("Expense deleted.")
        st.rerun()

    st.download_button(
        "Download expenses as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="expenses.csv",
        mime="text/csv"
    )

with st.expander("How it works"):
    st.write("This app uses Streamlit for the interface, SQLite for persistent storage, and parameterized SQL queries for database operations.")
