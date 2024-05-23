import discord
from discord.ext import commands
import os

from music_cog import MusicCog
from help_cog import HelpCog

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command('help')

async def setup():
    print("Loading cogs...")
    await bot.add_cog(HelpCog(bot))
    print("help_cog loaded")
    await bot.add_cog(MusicCog(bot))
    print("music_cog loaded")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def main():
    await setup()
    print("setup done")
    await bot.start(os.getenv("TOKEN"))

import asyncio
asyncio.run(main())