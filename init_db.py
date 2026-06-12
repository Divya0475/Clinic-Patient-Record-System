import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/database.db")

cursor = conn.cursor()

# Patients Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    phone TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    blood_group TEXT
)
""")

# Visits Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    doctor_name TEXT NOT NULL,

    clinic_name TEXT NOT NULL,

    clinic_phone TEXT NOT NULL,

    clinic_address TEXT,

    email TEXT UNIQUE,

    username TEXT UNIQUE,

    password TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")