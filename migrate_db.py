import sqlite3

def migrate():
    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE certificates ADD COLUMN branch TEXT DEFAULT 'Unknown Branch'")
        print("branch column added.")
    except sqlite3.OperationalError as e:
        print("branch column possibly already exists:", e)
        
    try:
        cursor.execute("ALTER TABLE certificates ADD COLUMN university TEXT DEFAULT 'Unknown University'")
        print("university column added.")
    except sqlite3.OperationalError as e:
        print("university column possibly already exists:", e)
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
