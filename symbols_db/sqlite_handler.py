import sqlite3
import datetime

conn = sqlite3.connect('blint.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS blintsboms
                 (purl char(100), time timestamp, sbom blob)''')

def store_sbom_in_sqlite(purl, sbom):
    
    c.execute("INSERT INTO blintsboms VALUES (?, ?, jsonb(?))", (purl, datetime.datetime.now(), sbom))
    conn.commit()
    conn.close()