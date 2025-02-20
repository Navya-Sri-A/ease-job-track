from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from calendar_integration import add_interview_to_calendar, add_reminder_to_calendar, delete_event_from_calendar 


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
            reminder_date TEXT,
            event_id_interview TEXT,  
            event_id_reminder TEXT   
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

        event_id_interview = None
        event_id_reminder = None

        if interview_date:
            event_id_interview = add_interview_to_calendar(company_name, job_title, interview_date)

        # Add reminder event to Google Calendar
        if reminder_date:
            event_id_reminder = add_reminder_to_calendar(company_name, job_title, reminder_date)


        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (company_name, job_title, application_status, applied_date, interview_date, reminder_date, event_id_interview, event_id_reminder)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (company_name, job_title, application_status,applied_date, interview_date, reminder_date, event_id_interview, event_id_reminder))
        conn.commit()
        conn.close()

        
        return redirect(url_for('index'))
    return render_template('add_job.html')

# Edit job details
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    conn = sqlite3.connect('job_tracker.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        company_name = request.form['company_name']
        job_title = request.form['job_title']
        application_status = request.form['application_status']
        applied_date = request.form['applied_date']
        interview_date = request.form['interview_date']
        reminder_date = request.form['reminder_date']

        cursor.execute('''
            UPDATE jobs
            SET company_name = ?, job_title = ?, application_status = ?, applied_date = ?, interview_date = ?, reminder_date = ?
            WHERE id = ?
        ''', (company_name, job_title, application_status, applied_date, interview_date, reminder_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM jobs WHERE id = ?", (id,))
    job = cursor.fetchone()
    conn.close()

    return render_template('edit_job.html', job=job)
    
# Delete a job
@app.route('/delete/<int:id>')
def delete_job(id):
    conn = sqlite3.connect('job_tracker.db')
    cursor = conn.cursor()

    cursor.execute("SELECT event_id_interview, event_id_reminder FROM jobs WHERE id = ?", (id,))
    event_ids = cursor.fetchone()

    if event_ids:
        event_id_interview, event_id_reminder = event_ids

        # Delete events from Google Calendar
        if event_id_interview:
            delete_event_from_calendar(event_id_interview)
        if event_id_reminder:
            delete_event_from_calendar(event_id_reminder)

    # Delete the job from the database
    cursor.execute("DELETE FROM jobs WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
