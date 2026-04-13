"""One-time seed script to insert the first student record."""
import sqlite3

conn = sqlite3.connect('certificates.db')
cursor = conn.cursor()
cursor.execute('''
    INSERT OR IGNORE INTO certificates
    (certificate_id, student_name, course_duration, company_name, start_date, end_date, company_logo_url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    'D27FD4D5435D4E6B',
    'Veerisetty Mahalakshmi',
    '8 Weeks',
    'CODTECH IT SOLUTIONS PRIVATE LIMITED',
    '19 January 2026',
    '15 March 2026',
    'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg'
))
conn.commit()
conn.close()
print("Seed data inserted successfully.")
