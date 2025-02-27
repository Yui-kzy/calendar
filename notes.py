import sqlite3
def get_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()  # 取得所有記事
    conn.close()
    return notes