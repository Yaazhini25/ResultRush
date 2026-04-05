from flask import Flask, render_template, request
import sqlite3
import time

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('results.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', student=None, results=None, error=None)
    
    # POST request
    reg_no = request.form.get('reg_no', '').strip()
    dob = request.form.get('dob', '').strip()
    
    # Simulate processing delay for load testing demo
    time.sleep(0.2)
    
    if not reg_no or not dob:
        return render_template('index.html', student=None, results=None, error='Invalid Register Number or DOB')
    
    conn = get_db_connection()
    
    # Query student
    student = conn.execute(
        'SELECT * FROM students WHERE reg_no = ? AND dob = ?',
        (reg_no, dob)
    ).fetchone()
    
    if student is None:
        conn.close()
        return render_template('index.html', student=None, results=None, error='Invalid Register Number or DOB')
    
    # Get results for this student
    results = conn.execute(
        'SELECT * FROM results WHERE reg_no = ? ORDER BY sub_code',
        (reg_no,)
    ).fetchall()
    
    conn.close()
    
    return render_template('index.html', student=student, results=results, error=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
