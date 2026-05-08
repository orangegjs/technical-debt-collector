import psycopg2

DB_URL = "postgresql://fundbridger_db_user:HQ7FTYaOpyBdQJ4CW3IWSFyJoBlNpLPL@dpg-d7kqcqlf420s73cte9a0-a.singapore-postgres.render.com/fundbridger_db"

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS fra_category (
        "categoryID"          SERIAL PRIMARY KEY,
        "categoryName"        VARCHAR UNIQUE NOT NULL,
        "categoryDescription" VARCHAR,
        "categoryStatus"      VARCHAR DEFAULT 'Active'
    );
""")

conn.commit()
conn.close()
print("Migration complete: fra_category table created.")
