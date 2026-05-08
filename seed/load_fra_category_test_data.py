import psycopg2
import os

DB_URL = "postgresql://fundbridger_db_user:HQ7FTYaOpyBdQJ4CW3IWSFyJoBlNpLPL@dpg-d7kqcqlf420s73cte9a0-a.singapore-postgres.render.com/fundbridger_db"

sql_path = os.path.join(os.path.dirname(__file__), "fra_category_test_data.sql")

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

with open(sql_path, "r", encoding="utf-8") as f:
    sql = f.read()

cur.execute(sql)
conn.commit()
conn.close()
print("Done: 9 FRA Category test records inserted.")
