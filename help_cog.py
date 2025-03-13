import discord
from discord.ext import commands

def __init__(self, bot):
    self.bot = bot
    self.help_message = """
**General Commands:**
`!help` - Displays all commands
`!p <keywords>` - Play a song from YouTube
`!skip` - Skip current song
`!pause`/`!resume` - Pause/Resume playback
`!q` - Show the queue
`!clear` - Clear the queue
`!leave` - Disconnect the bot
"""
    
@commands.command(name="help")
async def help(self, ctx):
    embed = discord.Embed(title="Help", description=self.help_message, color=0x00ff00)
    await ctx.send(embed=embed)