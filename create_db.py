"""
This file creates a database named expenses
"""

import sqlite3

# Establish connection
conn = sqlite3.connect("expenses.db")

# We want to have a cursor
cur = conn.cursor()

# Execute statement
# triple quotes is multi line string
cur.execute("""CREATE TABLE IF NOT EXISTS expenses 
(id INTEGER PRIMARY KEY,
Date DATE,
description TEXT,
category TEXT,
price REAL)""")

# Creating database
conn.commit()
conn.close()