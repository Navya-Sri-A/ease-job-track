from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('job_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            application_status TEXT NOT NULL,
            applied_date TEXT,
            interview_date TEXT,
            reminder_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect('job_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

# Add new job
@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        company_name = request.form['company_name']
        job_title = request.form['job_title']
        application_status = request.form['application_status']
        applied_date = request.form['applied_date']
        interview_date = request.form['interview_date']
        reminder_date = request.form['reminder_date']

        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (company_name, job_title, application_status, applied_date, interview_date, reminder_date)
            VALUES (?, ?, ?, ?,?, ?)
        ''', (company_name, job_title, application_status,applied_date, interview_date, reminder_date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('add_job.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
