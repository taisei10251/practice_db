import sqlite3
dbname = 'club_room.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, student_id TEXT, card_id TEXT, role TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, member_id INTEGER, card_id TEXT, name TEXT, entered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, exited_at TIMESTAMP)')

conn.commit()
conn.close()