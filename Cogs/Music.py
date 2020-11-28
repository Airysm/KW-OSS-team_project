#Music.py

import discord, asyncio, os, youtube_dl
from discord.ext import commands
from discord.voice_client import VoiceClient

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data=data
        self.title=data.get('title')
        self.url=data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, ),data=data)


class Music(commands.Cog, name='Music'):
    
    @commands.command(name='참가')
    async def join(self,ctx):
        if not ctx.message.author.voice:
            await ctx.send("음성채널에 참가하지 않았습니다")
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='퇴장')
    async def leave(self,ctx):
        await ctx.message.guild.voice_client.disconnect()

    @commands.command(name='노래')
    async def play(self,ctx,url):
        try:
            for filename in os.listdir("./"):
                if filename.endswith('.webm'):
                    os.remove(filename)
                    print("removed old song")
        except PermissionError:
            print("being played, can't remove")
            await ctx.send("현재 다른 노래가 재생 중입니다.")
            return
        
        channel = ctx.message.guild.voice_client
        song=await YTDLSource.from_url(url,loop=self.bot.loop)
        channel.play(song,after=lambda e: print("good song"))

        await ctx.send("노래를 재생합니다")

    @commands.command(name='중지')
    async def stop(self,ctx):
        channel = ctx.message.guild.voice_client
        channel.stop()

        await ctx.send("노래를 중지합니다")

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Music(bot))