import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

dbname = os.path.join(base_dir, 'club_room.db')
conn = sqlite3.connect(dbname)
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, student_id TEXT, card_id TEXT, role TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, card_id TEXT, name TEXT, entered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, exited_at TIMESTAMP)')
c.execute("INSERT INTO members (name, student_id, card_id, role) VALUES (?, ?, ?, ?)", ('山田太郎', '12345678', 'CARD001', '部員'))
c.execute("INSERT INTO members (name, student_id, card_id, role) VALUES (?, ?, ?, ?)", ('佐藤花子', '87654321', 'CARD002', '部員'))

conn.commit()
conn.close()
