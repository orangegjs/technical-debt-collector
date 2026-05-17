"""
Sprint 6 database migration.

Run from the backend/ directory (with venv active):
    python migrate_sprint6.py
"""
import sys
from sqlalchemy import text
from database import engine


SQL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS report (
        "reportID"      SERIAL  PRIMARY KEY,
        "reportType"    VARCHAR NOT NULL,
        "startDate"     DATE    NOT NULL,
        "endDate"       DATE    NOT NULL,
        "totalFRA"      INTEGER NOT NULL DEFAULT 0,
        "totalDonation" INTEGER NOT NULL DEFAULT 0,
        "totalAccount"  INTEGER NOT NULL DEFAULT 0
    )
    """,
]


def main():
    print("Running Sprint 6 migration...")
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
