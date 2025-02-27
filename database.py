import sqlite3

# 連接 SQLite（如果沒這個資料庫會自動建立）
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

# 建立記事表格（如果不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
)
''')

conn.commit()
conn.close()