import psycopg2

DB_URL = "postgresql://fundbridger_db_user:HQ7FTYaOpyBdQJ4CW3IWSFyJoBlNpLPL@dpg-d7kqcqlf420s73cte9a0-a.singapore-postgres.render.com/fundbridger_db"

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

cur.execute("ALTER TABLE user_account ADD COLUMN IF NOT EXISTS profile_picture_url TEXT;")

conn.commit()
conn.close()
print("Migration complete.")
