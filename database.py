import sqlite3

conn = sqlite3.connect('site.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT NOT NULL,
          email TEXT NOT NULL,
          password TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("database created successfully")