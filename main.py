from fastmcp import FastMCP
import aiosqlite
import sqlite3
import os
import json
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------

BASE_DIR = Path(__file__).parent
DB_PATH = os.environ.get("DB_PATH", str(BASE_DIR / "expenses.db"))

CATEGORIES_PATH = BASE_DIR / "categories.json"
mcp = FastMCP("Expense Tracker")


# -----------------------------
# Database Initialization
# -----------------------------
def init_db():
    """Initialize SQLite database."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
        )
        """)
        conn.commit()
    print(f"Database initialized: {DB_PATH}")

init_db()


# -----------------------------
# MCP Tools
# -----------------------------
@mcp.tool()
async def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    note: str = "",
):
    """Add a new expense."""

    try:
        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                INSERT INTO expenses
                (date, amount, category, subcategory, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    date,
                    amount,
                    category,
                    subcategory,
                    note,
                ),
            )

            await db.commit()

            return {
                "status": "success",
                "expense_id": cursor.lastrowid,
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_expenses(
    start_date: str,
    end_date: str,
):
    """List expenses between two dates."""

    try:
        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(
                """
                SELECT
                    id,
                    date,
                    amount,
                    category,
                    subcategory,
                    note
                FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC,id DESC
                """,
                (
                    start_date,
                    end_date,
                ),
            )

            rows = await cursor.fetchall()

            return [
                {
                    "id": r[0],
                    "date": r[1],
                    "amount": r[2],
                    "category": r[3],
                    "subcategory": r[4],
                    "note": r[5],
                }
                for r in rows
            ]

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def summarize(
    start_date: str,
    end_date: str,
    category: str | None = None,
):
    """Summarize expenses."""

    try:

        query = """
        SELECT
            category,
            SUM(amount),
            COUNT(*)
        FROM expenses
        WHERE date BETWEEN ? AND ?
        """

        params = [start_date, end_date]

        if category:
            query += " AND category=?"
            params.append(category)

        query += " GROUP BY category ORDER BY SUM(amount) DESC"

        async with aiosqlite.connect(DB_PATH) as db:

            cursor = await db.execute(query, params)

            rows = await cursor.fetchall()

            return [
                {
                    "category": r[0],
                    "total": r[1],
                    "count": r[2],
                }
                for r in rows
            ]

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


# -----------------------------
# MCP Resource
# -----------------------------
@mcp.resource("expense:///categories")
def categories():

    default_categories = {
        "categories": [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Healthcare",
            "Travel",
            "Education",
            "Business",
            "Other",
        ]
    }

    if CATEGORIES_PATH.exists():
        return CATEGORIES_PATH.read_text(encoding="utf-8")

    return json.dumps(default_categories, indent=2)


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )