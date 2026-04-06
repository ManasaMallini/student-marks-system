from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ✅ Create / Fix DB
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Drop old table (fix error)
    cursor.execute("DROP TABLE IF EXISTS students")

    # Create fresh table
    cursor.execute('''
        CREATE TABLE students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            student_id TEXT,
            s1 INTEGER,
            s2 INTEGER,
            s3 INTEGER
        )
    ''')

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        sid = request.form['student_id']
        s1 = int(request.form['s1'])
        s2 = int(request.form['s2'])
        s3 = int(request.form['s3'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, student_id, s1, s2, s3) VALUES (?, ?, ?, ?, ?)",
            (name, sid, s1, s2, s3)
        )

        conn.commit()
        conn.close()

        return redirect('/view')

    return render_template('add.html')


@app.route('/view')
def view():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()

    students = []

    for s in data:
        total = s[3] + s[4] + s[5]
        avg = total / 3

        if avg >= 90:
            grade = 'A'
        elif avg >= 75:
            grade = 'B'
        elif avg >= 50:
            grade = 'C'
        else:
            grade = 'Fail'

        students.append({
            'name': s[1],
            'student_id': s[2],
            'total': total,
            'average': avg,
            'grade': grade
        })

    return render_template('view.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)