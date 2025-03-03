import sqlite3

# 連線到 SQLite，若不存在則建立新的
conn = sqlite3.connect("day.db")
cursor = conn.cursor()

# 建立 users 表
cursor.execute("""
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
""")

# 建立 time_events 表
cursor.execute("""
CREATE TABLE time_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
""")

conn.commit()
conn.close()

print("✅ day.db 資料庫初始化完成！")

# 記事本資料庫
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

# 建立 notes 表
cursor.execute("""
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print("✅ notes.db 資料庫初始化完成！")