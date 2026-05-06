import psycopg2

DB_URL = "postgresql://fundbridger_db_user:HQ7FTYaOpyBdQJ4CW3IWSFyJoBlNpLPL@dpg-d7kqcqlf420s73cte9a0-a.singapore-postgres.render.com/fundbridger_db"

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Add profile_id FK column (nullable so existing accounts without a profile don't break)
cur.execute("""
    ALTER TABLE user_account
    ADD COLUMN IF NOT EXISTS profile_id INTEGER
    REFERENCES user_profile("profileID");
""")

# Migrate existing role strings to profile_id using the profileName match
cur.execute("""
    UPDATE user_account
    SET profile_id = up."profileID"
    FROM user_profile up
    WHERE user_account.role = up."profileName"
      AND user_account.profile_id IS NULL;
""")

conn.commit()
conn.close()
print("Migration complete: profile_id column added and existing roles mapped.")
print("Note: the old 'role' column is kept in the database for reference but is no longer used by the ORM.")
