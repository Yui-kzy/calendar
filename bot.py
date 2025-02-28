import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os 

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN1")  

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents = intents)

# 調用event函式庫
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")

    

@bot.tree.command(name="ping", description="查看機器人延遲")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # 計算機器人與 Discord 伺服器的延遲，轉換成毫秒
    await interaction.response.send_message(f"機器人延遲：{latency}ms")


bot.run(token)


# import discord
# from discord.ext import commands
# import sqlite3
# from dotenv import load_dotenv
# import os

# # 載入環境變數
# load_dotenv()
# token = os.getenv("DISCORD_BOT_TOKEN1")

# # 創建資料庫連接
# def create_db():
#     conn = sqlite3.connect('courses.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS courses (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER NOT NULL,
#                     course_name TEXT NOT NULL,
#                     course_time TEXT NOT NULL,
#                     course_location TEXT NOT NULL)''')
#     conn.commit()
#     conn.close()

# # 新增課程資料
# def add_course(user_id, course_name, course_time, course_location):
#     conn = sqlite3.connect('courses.db')
#     c = conn.cursor()
#     c.execute('''INSERT INTO courses (user_id, course_name, course_time, course_location)
#                  VALUES (?, ?, ?, ?)''', (user_id, course_name, course_time, course_location))
#     conn.commit()
#     conn.close()

# # 查詢用戶課程
# def get_courses(user_id):
#     conn = sqlite3.connect('courses.db')
#     c = conn.cursor()
#     c.execute('''SELECT course_name, course_time, course_location FROM courses WHERE user_id = ?''', (user_id,))
#     courses = c.fetchall()
#     conn.close()
#     return courses

# # 設定機器人
# intents = discord.Intents.default()
# bot = commands.Bot(command_prefix="!", intents=intents)

# # 當機器人啟動時初始化資料庫
# @bot.event
# async def on_ready():
#     print(f"{bot.user} 已啟動！")
#     create_db()  # 初始化資料庫

# # 查看課程指令
# @bot.command()
# async def view_courses(ctx):
#     user_id = ctx.author.id
#     courses = get_courses(user_id)
#     if courses:
#         response = "你的課程有：\n"
#         for course in courses:
#             response += f"課程名稱: {course[0]}, 上課時間: {course[1]}, 上課地點: {course[2]}\n"
#         await ctx.send(response)
#     else:
#         await ctx.send("你尚未設定課程！")

# # 新增課程指令
# @bot.command()
# async def add_course(ctx, course_name: str, course_time: str, course_location: str):
#     user_id = ctx.author.id
#     add_course(user_id, course_name, course_time, course_location)
#     await ctx.send(f"已成功新增課程：{course_name}，時間：{course_time}，地點：{course_location}")

# bot.run(token)