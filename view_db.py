import sqlite3

conn = sqlite3.connect('results.db')
cursor = conn.cursor()

# show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# show some data
cursor.execute("SELECT * FROM students LIMIT 5;")
print(cursor.fetchall())

conn.close()