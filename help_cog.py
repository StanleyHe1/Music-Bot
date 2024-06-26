import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
!help - displays all the available commands
!q - displays the current music queue
!p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
!skip - skips the current song being played
!clear - Stops the music and clears the queue
!leave - Disconnect the bot from the voice channel
!pause - pauses the current song being played or resumes if already paused
!resume - resumes playing the current song
```
"""
        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        pass
    
    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)
        
    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)
    