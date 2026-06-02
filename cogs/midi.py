import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import re

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "samples")

def get_sample_path(note: str):
    match = re.match(r'^([A-Ga-g][#b]?)(\d)$', note.strip())
    if not match:
        return None
    name = match.group(1).lower()
    octave = match.group(2)
    filename = f"{name}{octave}.wav"
    filepath = os.path.join(SAMPLES_DIR, filename)
    return filepath if os.path.exists(filepath) else None

class Midi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="midi", description="미디가 피아노를 연주해줌")
    @app_commands.describe(notes="예: C4-D4-E4 또는 C4---C4")
    async def midi(self, interaction: discord.Interaction, notes: str):
        vc = interaction.guild.voice_client

        if not vc:
            channel = interaction.user.voice.channel if interaction.user.voice else None
            if not channel:
                return await interaction.response.send_message("먼저 음성 채널에 들어가줘!", ephemeral=True)
            vc = await channel.connect()

        await interaction.response.send_message(f"미디가 연주를 시작합니다! ({notes})")

        tokens = re.split(r'(-+)', notes)
        note_list = []
        for token in tokens:
            if re.match(r'^-+$', token):
                note_list.append(("delay", len(token)))
            elif token.strip():
                note_list.append(("note", token.strip()))

        for kind, val in note_list:
            if kind == "delay":
                await asyncio.sleep(val * 0.1)
            else:
                path = get_sample_path(val)
                if not path:
                    print(f"샘플 없음: {val}")
                    continue
                source = discord.FFmpegPCMAudio(path)
                vc.play(source)
                while vc.is_playing():
                    await asyncio.sleep(0.05)
                await asyncio.sleep(0.05)

async def setup(bot):
    await bot.add_cog(Midi(bot))
