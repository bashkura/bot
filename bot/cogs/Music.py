import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        # Check if the author is in a voice channel
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect(reconnect=True)
            source = FFmpegPCMAudio('song/gamarjoba.mp3')
            player = voice.play(source)
            await ctx.send(f"Joined {channel.name}")
        else:
            await ctx.send("You must be in a voice channel to run this command")

    @commands.command()
    async def leave(self, ctx):
        # Check if the bot is in a voice channel
        if ctx.voice_client:
            # Disconnect from the voice channel
            await ctx.voice_client.disconnect()
            await ctx.send("Left the voice channel")
        else:
            await ctx.send("I am not in a voice channel")
    
    @commands.command()
    async def pause(self, ctx):
        voice = ctx.voice_client
        if voice.is_playing():
            voice.pause()

    @commands.command()
    async def resume(self, ctx):
        voice = ctx.voice_client
        if voice.is_paused():
            voice.resume()

    @commands.command()
    async def stop(self, ctx):
        voice = ctx.voice_client
        if voice.is_playing() or voice.is_paused():
            voice.stop()
            await ctx.send("Audio stopped")
    
    @commands.command()
    async def play(self, ctx, arg):
        voice = ctx.voice_client
        song = arg + '.mp3'
        source = FFmpegPCMAudio("song/" + song)
        player = voice.play(source)
        
async def setup(bot):
    await bot.add_cog(Music(bot))
