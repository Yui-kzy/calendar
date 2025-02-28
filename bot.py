import discord
from discord import app_commands
from discord.ext import commands , tasks
from dotenv import load_dotenv
import sqlite3
import os
import datetime

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN1")

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 調用event函式庫
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"同步了 {len(synced)} 個應用命令")
    except Exception as e:
        print(f"同步應用命令時發生錯誤: {e}")
    check_exams.start()

# 查看延遲
@bot.tree.command(name="ping", description="查看機器人延遲")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # 計算機器人與 Discord 伺服器的延遲，轉換成毫秒
    await interaction.response.send_message(f"機器人延遲：{latency}ms")

# 新增課表指令
@bot.tree.command(name="add_schedule", description="新增課表")
async def add_schedule(interaction: discord.Interaction, subject: str, date: str):
    user_id = interaction.user.id
    conn = sqlite3.connect("day.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schedule (user_id, subject, date) VALUES (?, ?, ?)", (user_id, subject, date))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"已新增課表: {subject} 在 {date}")


# 新增考試指令
@bot.tree.command(name="add_exam", description="新增考試")
async def add_exam(interaction: discord.Interaction, subject: str, date: str):
    user_id = interaction.user.id
    try:
        # 確保日期格式正確
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await interaction.response.send_message("日期格式錯誤，請使用 YYYY-MM-DD 格式")
        return

    conn = sqlite3.connect("day.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO exams (user_id, subject, date) VALUES (?, ?, ?)", (user_id, subject, date))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"已新增考試: {subject} 在 {date}")


# 查詢考試剩餘時間指令
@bot.tree.command(name="exam_countdown", description="查詢考試剩餘時間")
async def exam_countdown(interaction: discord.Interaction):
    user_id = interaction.user.id
    conn = sqlite3.connect("day.db")
    cursor = conn.cursor()
    cursor.execute("SELECT subject, date FROM exams WHERE user_id = ?", (user_id,))
    exams = cursor.fetchall()
    conn.close()

    today = datetime.date.today()
    response = "考試倒數:\n"
    for subject, date_str in exams:
        exam_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        days_left = (exam_date - today).days
        response += f"{subject}: 還有 {days_left} 天\n"

    await interaction.response.send_message(response)

# 定時提醒功能
@tasks.loop(hours=24)
async def check_exams():
    await bot.wait_until_ready()
    conn = sqlite3.connect("day.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, subject, date FROM exams")
    exams = cursor.fetchall()
    conn.close()

    today = datetime.date.today()
    for user_id, subject, date_str in exams:
        exam_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        days_left = (exam_date - today).days
        if days_left == 1:
            user = await bot.fetch_user(user_id)
            await user.send(f"提醒: 明天有 {subject} 考試!")


bot.run(token)
