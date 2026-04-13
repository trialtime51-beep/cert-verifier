import sqlite3
conn = sqlite3.connect('certificates.db')
cursor = conn.cursor()
cursor.execute('UPDATE certificates SET company_logo_url = ? WHERE certificate_id = ?', ('https://www.uww.edu/images/career/Logos/Forage%20Logo.png', 'D27FD4D5435D4E6B'))
conn.commit()
conn.close()
