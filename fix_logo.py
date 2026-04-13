import sqlite3
# Update all certificates to use a reliable working logo
conn = sqlite3.connect('certificates.db')
conn.execute("UPDATE certificates SET company_logo_url = 'https://cdn.worldvectorlogo.com/logos/the-forage.svg'")
conn.commit()
conn.close()
print("All logos updated successfully!")
