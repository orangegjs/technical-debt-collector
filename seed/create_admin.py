import psycopg2
import bcrypt

DB_URL = "postgresql://fundbridger_db_user:HQ7FTYaOpyBdQJ4CW3IWSFyJoBlNpLPL@dpg-d7kqcqlf420s73cte9a0-a.singapore-postgres.render.com/fundbridger_db"
USERNAME = "admin"
PASSWORD = "Admin@123456"
EMAIL = "admin@fundbridger.com"

hashed = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt()).decode()

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()
cur.execute(
    'INSERT INTO user_account (username, email, password, "accountStatus", role) VALUES (%s, %s, %s, %s, %s)',
    (USERNAME, EMAIL, hashed, "Active", "User Admin"),
)
conn.commit()
conn.close()
print("Admin account created successfully.")
print(f"  Username: {USERNAME}")
print(f"  Password: {PASSWORD}")
