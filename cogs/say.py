import discord
from discord import app_commands
from discord.ext import commands
import json
import os

OWNER_ID = 968837432617365564
STATE_PATH = os.path.join("data", "state.json")

def load_state():
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_only = False

    @app_commands.command(name="say", description="입력한 문장을 미디가 말해줌!!")
    @app_commands.describe(message="미디가 말할 문장")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @app_commands.command(name="saytoggle", description="SAY (채팅) 명령어를 켜거나 끔!")
    async def saytoggle(self, interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("이건 히원만 가능해!", ephemeral=True)
        state = load_state()
        state["sayEnabled"] = not state.get("sayEnabled", False)
        save_state(state)
        status = "켜짐" if state["sayEnabled"] else "꺼짐"
        await interaction.response.send_message(f"SAY 명령어 {status}!")

    @app_commands.command(name="toggle", description="모든 명령어를 히원만 쓸 수 있게 하거나 해제함!")
    async def toggle(self, interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("이건 히원만 가능해!", ephemeral=True)
        self.owner_only = not self.owner_only
        await interaction.response.send_message(f"이제 {'히원만' if self.owner_only else '모두'} 사용 가능!")

async def setup(bot):
    await bot.add_cog(Say(bot))
