"""
Add a student to the certificate database and generate their personal QR code.
Usage: python add_student.py
"""
import sqlite3
import os
import uuid
import qrcode
from PIL import Image

BASE_URL = "https://cert-verifier-1z6c.onrender.com"  # Live deployment URL

def generate_cert_id():
    """Generate a unique 16-character hex certificate ID."""
    return uuid.uuid4().hex[:16].upper()

def add_student(student_name, course_duration, company_name, start_date, end_date, logo_url, university, internship_name, cert_id=None):
    if not cert_id:
        cert_id = generate_cert_id()

    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO certificates (certificate_id, student_name, course_duration, company_name, start_date, end_date, company_logo_url, university, internship_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cert_id, student_name, course_duration, company_name, start_date, end_date, logo_url, university, internship_name))
        conn.commit()
        print(f"\n✅ Student '{student_name}' added successfully!")
        print(f"   Certificate ID: {cert_id}")
    except sqlite3.IntegrityError:
        print(f"❌ Error: Certificate ID '{cert_id}' already exists.")
        conn.close()
        return
    conn.close()

    # Generate QR code
    url = f"{BASE_URL}/verify/{cert_id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    safe_name = student_name.replace(" ", "_")
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"qr_{safe_name}_{cert_id}.png")
    img.save(out_path)
    print(f"   QR Code saved to: {out_path}")
    print(f"   Verification URL: {url}\n")

if __name__ == "__main__":
    print("=== Certificate Verification System — Add Student ===\n")
    name = input("Student Name: ").strip()
    duration = input("Course Duration (e.g., 8 Weeks): ").strip()
    company = input("Company Name (e.g., CODTECH IT SOLUTIONS PRIVATE LIMITED): ").strip()
    logo = input("Company Logo URL (optional, leave blank for no logo): ").strip()
    start = input("Start Date (e.g., 19 January 2026): ").strip()
    end = input("End Date (e.g., 15 March 2026): ").strip()
    university = input("University (e.g., XYZ University): ").strip()
    internship_name = input("Internship Name (e.g., EY Technology Risk Virtual Internship): ").strip()

    add_student(name, duration, company, start, end, logo, university, internship_name)
