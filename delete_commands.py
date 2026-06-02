import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CLIENT_ID = "1146044273419096154"
GUILD_ID = "1360789767771656202"  # JS .env에서 가져온 GUILD_ID

async def delete_all_commands():
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        # 전역 커맨드 삭제
        url_global = f"https://discord.com/api/v10/applications/{CLIENT_ID}/commands"
        async with session.put(url_global, headers=headers, json=[]) as res:
            if res.ok:
                print("전역 커맨드 삭제됨!")
            else:
                print(f"전역 실패: {res.status} - {await res.text()}")

        # 길드 커맨드 삭제
        url_guild = f"https://discord.com/api/v10/applications/{CLIENT_ID}/guilds/{GUILD_ID}/commands"
        async with session.put(url_guild, headers=headers, json=[]) as res:
            if res.ok:
                print("길드 커맨드 삭제됨!")
            else:
                print(f"길드 실패: {res.status} - {await res.text()}")

asyncio.run(delete_all_commands())
