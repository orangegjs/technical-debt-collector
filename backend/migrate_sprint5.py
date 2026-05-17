"""
Sprint 5 database migration.

Run from the backend/ directory (with venv active):
    python migrate_sprint5.py
"""

import sys
from sqlalchemy import text
from database import engine


SQL_STATEMENTS = [
    'ALTER TABLE fra_activity ADD COLUMN IF NOT EXISTS "fraViewCount" INTEGER DEFAULT 0',
    'ALTER TABLE fra_activity ADD COLUMN IF NOT EXISTS "fraShortlistCount" INTEGER DEFAULT 0',
    """
    CREATE TABLE IF NOT EXISTS favourite (
        "favouriteID" SERIAL PRIMARY KEY,
        "savedDate"   DATE    NOT NULL DEFAULT CURRENT_DATE,
        "fraID"       INTEGER NOT NULL REFERENCES fra_activity("fraID"),
        "userID"      INTEGER NOT NULL REFERENCES user_account("userID"),
        UNIQUE ("userID", "fraID")
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS donation (
        "donationID"     SERIAL PRIMARY KEY,
        "donationAmount" DECIMAL(12,2) NOT NULL CHECK ("donationAmount" > 0),
        "donationDate"   DATE NOT NULL,
        "donationStatus" VARCHAR DEFAULT 'Completed',
        "fraID"          INTEGER NOT NULL REFERENCES fra_activity("fraID"),
        "userID"         INTEGER NOT NULL REFERENCES user_account("userID")
    )
    """,
]


def main():
    print("Running Sprint 5 migration...")
    try:
        with engine.begin() as conn:
            for stmt in SQL_STATEMENTS:
                conn.execute(text(stmt))
                print(f"  OK: {stmt.strip()[:60]}...")
        print("Migration complete.")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
