import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

# main.py 기준 절대경로로 고정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# data/state.json 없으면 자동 생성
STATE_PATH = os.path.join("data", "state.json")
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(STATE_PATH):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump({"sayEnabled": False}, f)

@bot.event
async def on_ready():
    print(f"로그인 완료! {bot.user}")

# SAY 채팅 명령어 처리
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content.startswith("SAY "):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
        if not state.get("sayEnabled", False):
            return
        text = message.content[4:].strip()
        if text:
            await message.channel.send(text)
            try:
                await message.delete()
            except Exception:
                pass
        return

    await bot.process_commands(message)

async def main():
    async with bot:
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"  cog 로드: {filename}")
        await bot.login(TOKEN)
        await bot.tree.sync()
        print("슬래시 커맨드 등록 완료!")
        await bot.connect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
