import discord
from discord import app_commands
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="join", description="미디를 음챗으로 부름")
    async def join(self, interaction: discord.Interaction):
        try:
            channel = interaction.user.voice.channel if interaction.user.voice else None
            if not channel:
                return await interaction.response.send_message("먼저 음성 채널에 들어가줘", ephemeral=True)
            await channel.connect()
            await interaction.response.send_message(f"{channel.name} 에 미디 입장!")
        except Exception as e:
            print(f"join 에러: {e}")
            await interaction.response.send_message(f"에러남: {e}", ephemeral=True)

    @app_commands.command(name="leave", description="미디를 음챗에서 내보냄")
    async def leave(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if not vc:
            return await interaction.response.send_message("아무 음성 채널에도 없는데?? 뭐임", ephemeral=True)
        await vc.disconnect()
        await interaction.response.send_message("ㅂㅂ")

async def setup(bot):
    await bot.add_cog(Voice(bot))
