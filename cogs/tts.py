import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import os
import asyncio

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="tts", description="미디가 말함 !!")
    @app_commands.describe(message="봇이 말할 문장")
    async def tts(self, interaction: discord.Interaction, message: str):
        vc = interaction.guild.voice_client
        if not vc:
            return await interaction.response.send_message("먼저 `/join`으로 음성 채널에 불러줘", ephemeral=True)

        await interaction.response.defer()

        api_key = os.getenv("ELEVENLABS_API_KEY")
        voice_id = os.getenv("ELEVENLABS_VOICE_ID")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                    json={"text": message, "model_id": "eleven_multilingual_v2"}
                ) as res:
                    if not res.ok:
                        raise Exception(f"API 오류: {res.status}")
                    audio_data = await res.read()

            filepath = f"tts_{interaction.id}.mp3"
            with open(filepath, "wb") as f:
                f.write(audio_data)

            source = discord.FFmpegPCMAudio(filepath)
            vc.play(source)

            await interaction.followup.send(f'"{message}"')

            # 재생 끝나면 파일 삭제
            while vc.is_playing():
                await asyncio.sleep(0.1)
            os.remove(filepath)

        except Exception as e:
            print(e)
            await interaction.followup.send("이거 TTS 오류남 고쳐 시1발")

async def setup(bot):
    await bot.add_cog(TTS(bot))
