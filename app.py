from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certificates.db')

def init_db():
    """Initialize DB and seed first student if table is empty."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            certificate_id TEXT PRIMARY KEY,
            student_name TEXT NOT NULL,
            course_duration TEXT NOT NULL,
            company_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            company_logo_url TEXT,
            branch TEXT,
            university TEXT,
            internship_name TEXT
        )
    ''')
    # Seed the first student
    cursor.execute('''
        INSERT OR IGNORE INTO certificates
        (certificate_id, student_name, course_duration, company_name, start_date, end_date, company_logo_url, branch, university, internship_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'D27FD4D5435D4E6B',
        'Veerisetty Mahalakshmi',
        '8 Weeks',
        'CODTECH IT SOLUTIONS PRIVATE LIMITED',
        '19 January 2026',
        '15 March 2026',
        'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg',
        'Unknown Branch',
        'Unknown University',
        'Technical Internship'
    ))
    conn.commit()
    conn.close()

def get_certificate(cert_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM certificates WHERE certificate_id = ?', (cert_id.upper(),))
    row = cursor.fetchone()
    conn.close()
    return row

@app.route('/verify/<cert_id>')
def verify(cert_id):
    cert = get_certificate(cert_id)
    if cert:
        return render_template('verify.html', cert=cert)
    else:
        return render_template('invalid.html', scanned_id=cert_id.upper()), 404

@app.route('/')
def index():
    return '<h3>Certificate Verification System</h3><p>Visit <code>/verify/&lt;CERTIFICATE_ID&gt;</code> to verify a certificate.</p>'

# Initialize DB on startup
init_db()

if __name__ == '__main__':
    app.run(debug=True)
