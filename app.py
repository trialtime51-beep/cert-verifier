from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_in_production'

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certificates.db')

def init_db():
    """Initialize DB and seed first student if table is empty."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create certificates table
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
            internship_name TEXT,
            student_email TEXT
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            name TEXT
        )
    ''')
    
    # Add student_email column if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE certificates ADD COLUMN student_email TEXT")
    except sqlite3.OperationalError:
        pass # Column likely already exists
        
    # Seed the first student certificate
    cursor.execute('''
        INSERT OR IGNORE INTO certificates
        (certificate_id, student_name, course_duration, company_name, start_date, end_date, company_logo_url, branch, university, internship_name, student_email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        'Technical Internship',
        'student@example.com'
    ))
    
    # Seed default Admin
    admin_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password_hash, role, name)
        VALUES (?, ?, ?, ?)
    ''', ('admin@forage.com', admin_hash, 'admin', 'Administrator'))
    
    # Seed a default Student to match the certificate
    student_hash = generate_password_hash('student123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password_hash, role, name)
        VALUES (?, ?, ?, ?)
    ''', ('student@example.com', student_hash, 'student', 'Veerisetty Mahalakshmi'))

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_certificate(cert_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM certificates WHERE certificate_id = ?', (cert_id.upper(),)).fetchone()
    conn.close()
    return row

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['role']
            session['name'] = user['name']
            
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    if session.get('role') == 'admin':
        certificates = conn.execute('SELECT * FROM certificates').fetchall()
        conn.close()
        return render_template('dashboard_admin.html', certificates=certificates)
    else:
        email = session.get('email')
        certificates = conn.execute('SELECT * FROM certificates WHERE student_email = ?', (email,)).fetchall()
        conn.close()
        return render_template('dashboard_student.html', certificates=certificates)

@app.route('/verify/<cert_id>')
def verify(cert_id):
    cert = get_certificate(cert_id)
    if cert:
        return render_template('verify.html', cert=cert)
    else:
        return render_template('invalid.html', scanned_id=cert_id.upper()), 404

@app.route('/')
def index():
    return render_template('index.html')

# Initialize DB on startup
init_db()

if __name__ == '__main__':
    app.run(debug=True)
