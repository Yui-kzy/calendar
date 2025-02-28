import sqlite3

# 建立資料庫連接
conn = sqlite3.connect("day.db")
cursor = conn.cursor()

# 建立課表表格（如果不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    date TEXT NOT NULL
)
''')

# 建立考試表格（如果不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    date TEXT NOT NULL
)
''')

# 提交變更並關閉連接
conn.commit()
conn.close()

print("資料庫初始化完成")