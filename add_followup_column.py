import sqlite3

conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE visits
ADD COLUMN followup_date TEXT
""")

conn.commit()
conn.close()

print("followup_date column added successfully")