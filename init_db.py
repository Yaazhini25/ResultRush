import sqlite3
import random
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect('results.db')
cursor = conn.cursor()

# Drop existing tables
cursor.execute('DROP TABLE IF EXISTS results')
cursor.execute('DROP TABLE IF EXISTS students')

# Create tables
cursor.execute('''
    CREATE TABLE students (
        reg_no TEXT PRIMARY KEY,
        dob TEXT,
        name TEXT,
        sem INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reg_no TEXT,
        sub_code TEXT,
        sub_name TEXT,
        grade TEXT,
        result TEXT,
        FOREIGN KEY (reg_no) REFERENCES students(reg_no)
    )
''')

# Fixed subjects for semester 5
subjects = [
    ('CS501', 'DBMS'),
    ('CS502', 'Operating Systems'),
    ('CS503', 'Computer Networks'),
    ('CS504', 'Algorithms'),
    ('CS505', 'Software Engineering')
]

# Generate DOB range
start_date = datetime(2004, 1, 10)
end_date = datetime(2004, 1, 28)

# Insert 5000 students
for i in range(1000, 6000):
    reg_no = str(i)
    
    # Random DOB between 2004-01-10 and 2004-01-28
    random_days = random.randint(0, (end_date - start_date).days)
    dob = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
    
    # Simple name
    name = f'Student {i}'
    sem = 5
    
    cursor.execute('INSERT INTO students VALUES (?, ?, ?, ?)',
                   (reg_no, dob, name, sem))
    
    # Insert 5 subject results for each student
    for sub_code, sub_name in subjects:
        # Random grade: 40% A, 30% B, 20% C, 5% D, 5% F
        rand = random.random()
        if rand < 0.4:
            grade = 'A'
        elif rand < 0.7:
            grade = 'B'
        elif rand < 0.9:
            grade = 'C'
        elif rand < 0.95:
            grade = 'D'
        else:
            grade = 'F'
        
        result = 'Fail' if grade == 'F' else 'Pass'
        
        cursor.execute('INSERT INTO results (reg_no, sub_code, sub_name, grade, result) VALUES (?, ?, ?, ?, ?)',
                       (reg_no, sub_code, sub_name, grade, result))

conn.commit()
conn.close()

print('✅ Database created with 5000 students')
