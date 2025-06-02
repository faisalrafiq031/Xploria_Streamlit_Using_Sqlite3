import sqlite3
import pandas as pd
import os

# Create a new SQLite database or connect to existing one
db_path = r"D:\Data Engineer Internship CodeGurus\SQL - DATA ENGINEERING\Streamlit-sqlite3\data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sample data for 'emp' table
emp_data = [
    (1, "Alice", "HR", 50000),
    (2, "Bob", "Engineering", 75000),
    (3, "Charlie", "Sales", 60000),
    (4, "David", "Engineering", 72000),
    (5, "Eve", "HR", 52000),
    (6, "Frank", "Marketing", 58000),
    (7, "Grace", "Sales", 61000),
    (8, "Heidi", "Engineering", 74000),
    (9, "Ivan", "Marketing", 57000),
    (10, "Judy", "HR", 53000),
    (11, "Karl", "Engineering", 76000),
    (12, "Laura", "Sales", 62000),
    (13, "Mallory", "Engineering", 77000),
    (14, "Niaj", "HR", 54000),
    (15, "Olivia", "Marketing", 59000),
    (16, "Peggy", "Sales", 63000),
    (17, "Quentin", "Engineering", 78000),
    (18, "Rupert", "HR", 55000),
    (19, "Sybil", "Sales", 64000),
    (20, "Trent", "Marketing", 60000),
]

# Create and populate 'emp' table
cursor.execute("DROP TABLE IF EXISTS emp")
cursor.execute("""
    CREATE TABLE emp (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER
    )
""")
cursor.executemany("INSERT INTO emp VALUES (?, ?, ?, ?)", emp_data)

# Sample data for 'staff' table
staff_data = [
    (101, "Admin1", "Administrator", "admin1@xploria.com"),
    (102, "Admin2", "Administrator", "admin2@xploria.com"),
    (103, "Mod1", "Moderator", "mod1@xploria.com"),
    (104, "Mod2", "Moderator", "mod2@xploria.com"),
    (105, "Support1", "Support", "support1@xploria.com"),
    (106, "Support2", "Support", "support2@xploria.com"),
    (107, "Tech1", "Technician", "tech1@xploria.com"),
    (108, "Tech2", "Technician", "tech2@xploria.com"),
    (109, "HR1", "HR", "hr1@xploria.com"),
    (110, "HR2", "HR", "hr2@xploria.com"),
    (111, "Admin3", "Administrator", "admin3@xploria.com"),
    (112, "Mod3", "Moderator", "mod3@xploria.com"),
    (113, "Support3", "Support", "support3@xploria.com"),
    (114, "Tech3", "Technician", "tech3@xploria.com"),
    (115, "HR3", "HR", "hr3@xploria.com"),
    (116, "Admin4", "Administrator", "admin4@xploria.com"),
    (117, "Mod4", "Moderator", "mod4@xploria.com"),
    (118, "Support4", "Support", "support4@xploria.com"),
    (119, "Tech4", "Technician", "tech4@xploria.com"),
    (120, "HR4", "HR", "hr4@xploria.com"),
]

# Create and populate 'staff' table
cursor.execute("DROP TABLE IF EXISTS staff")
cursor.execute("""
    CREATE TABLE staff (
        staff_id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        email TEXT
    )
""")
cursor.executemany("INSERT INTO staff VALUES (?, ?, ?, ?)", staff_data)

conn.commit()
conn.close()

db_path  

