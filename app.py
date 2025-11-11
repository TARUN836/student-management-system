try:
    from flask import Flask, render_template, request, redirect
except ImportError as e:
    raise RuntimeError("Flask is not installed. Install it with: pip install flask (and activate your virtualenv if used).") from e

import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  department TEXT,
                  age INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        dept = request.form['department']
        age = request.form['age']
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, department, age) VALUES (?, ?, ?)", (name, dept, age))
        conn.commit()
        conn.close()
        return redirect('/view')
    return render_template('add_student.html')

@app.route('/view')
def view_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return render_template('view_students.html', students=data)
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
