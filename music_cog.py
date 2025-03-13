import discord
from discord.ext import commands

from yt_dlp import YoutubeDL

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self, item):
        try:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
                return {'source': info['url'], 'title': info['title']}
        except Exception:
            return None  # Use None instead of False
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        try:
            if len(self.music_queue) > 0:
                self.is_playing = True
                m_url = self.music_queue[0][0]['source']
                if self.vc is None or not self.vc.is_connected():
                    try:
                        self.vc = await self.music_queue[0][1].connect()
                    except Exception as e:
                        await ctx.send(f"Failed to connect: {e}")
                        return
                else:
                    await self.vc.move_to(self.music_queue[0][1])
                self.music_queue.pop(0)
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.play_next())
                await ctx.send(f"**Now Playing:** {self.music_queue[0][0]['title']}")  # Add now playing message
            else:
                self.is_playing = False
        except Exception as err:
            print(f"Error: {err}")
    
    @commands.command(name='play', aliases=['p', 'playing'], help='Play the selected song from youtube')
    async def play(self, ctx, *args):
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel to use this command.")
            return
        voice_channel = ctx.author.voice.channel
        query = ' '.join(args)
        if voice_channel is None:
            await ctx.send("Connect to a voice channel pleace")
            return
        if self.vc and self.vc.is_connected() and self.vc.channel != voice_channel:
            await ctx.send("Already in another voice channel!")
            return
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if song is None:
                await ctx.send("Could not find the song.")
                return
            if type(song) == type(True):
                await ctx.send("Incorrect format, try a different keyword")
                return
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)
                    await ctx.send(f"**Now Playing:** {self.music_queue[0][0]['title']}")
                    return

    @commands.command(name='pause', help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name='resume', aliases=['r'], help="Resumes the current song being played")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="skip", aliases=['s'], help='Skips the currently playing song')
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name='queue', aliases=['q'], help='Displays all the songs in the queue')
    async def queue(self, ctx):
        retval = ''
        for i in range(0, len(self.music_queue)):
            if i > 4: 
                break
            retval += self.music_queue[i][0]['title'] + '\n'
        if retval != '':
            await ctx.send(retval)
        else:
            await ctx.send("No music in the queue")

    @commands.command(name='clear', aliases=['c', 'bin'], help="Stops the current song and clears the queue")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")

    @commands.command(name="leave", help="Disconnect the bot")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []  # Clear the queue
        if self.vc:
            await self.vc.disconnect()
