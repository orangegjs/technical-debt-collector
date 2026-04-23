import psycopg2

DB_URL = "postgresql://fundbridger_db_user:HQ7FTYaOpyBdQJ4CW3IWSFyJoBlNpLPL@dpg-d7kqcqlf420s73cte9a0-a.singapore-postgres.render.com/fundbridger_db"

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

with open("seed_data.sql", encoding="utf-8") as f:
    sql = f.read()

inserted = 0
skipped = 0

for line in sql.splitlines():
    line = line.strip()
    if not line or line.startswith("--"):
        continue
    try:
        cur.execute(line)
        conn.commit()
        inserted += 1
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        skipped += 1

conn.close()
print(f"Done. Inserted: {inserted}, Skipped (duplicates): {skipped}")
