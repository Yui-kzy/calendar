import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import os

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

@bot.tree.command(name="ping", description="查看機器人延遲")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # 計算機器人與 Discord 伺服器的延遲，轉換成毫秒
    await interaction.response.send_message(f"機器人延遲：{latency}ms")

bot.run(token)
