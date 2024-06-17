import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = {}
    
    def check_queue(self, ctx, id):
        if self.queues[id] != []:
            voice = ctx.guild.voice_client
            source = self.queues[id].pop(0)
            voice.play(source)
            
    @commands.command(pass_context = True)
    async def join(self, ctx):
        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            ffmpeg_options = {
                'before_options': '-loglevel debug',  # This will print debug information
                'options': '-vn'
            }
            source = FFmpegPCMAudio('inspire.wav', **ffmpeg_options)
            print(source)
            player = PCMVolumeTransformer(source, volume=1.0)
            print(player)
            try:
                voice.play(player)
                await ctx.send("I joined the voice channel and started playing audio.")
                await ctx.send("Finished playing audio.")
                
            except Exception as e:
                await ctx.send(f"An error occurred while trying to play audio: {str(e)}")
        else:
            await ctx.send("You aren't in a voice channel u have to be in a voice channel to run this command.")
            
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if(ctx.voice_client):
            await ctx.guild.voice_client.disconnect()    
            await ctx.send("left the channel")
        else:
            await ctx.send("I aim't in a voice channel")
            
    @commands.command(pass_context = True)
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild= ctx.guild)
        if voice.is_playing():
            voice.pause()
        else: 
            await ctx.send("I am not playing any audio")
            
    @commands.command(pass_context = True)
    async def resume(self, ctx):
        voice =  discord.utils.get(self.client.voice_clients, guild= ctx.guild)
        if voice.is_paused():
            voice.resume()
        else: 
            await ctx.send("I am not playing any audio")
            
    @commands.command(pass_context = True)
    async def stop(self, ctx):
        voice =  discord.utils.get(self.client.voice_clients, guild= ctx.guild)
        if voice.is_playing():
            voice.stop()
            await ctx.send("i Stopped the audio")
        else: 
            await ctx.send("I am not playing any audio")
            
    @commands.command(pass_context = True)
    async def play(self, ctx, arg):
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(arg + ".wav")
        player = PCMVolumeTransformer(source, volume=1.0)
        voice.play(player, after= lambda x = None: self.check_queue(ctx, ctx.message.guild.id))
        
    @commands.command(pass_context=True)
    async def queue(self, ctx, arg):
        voice = ctx.guild.voice_client
        song = arg + ".wav"
        source = FFmpegPCMAudio(song)
        
        guild_id = ctx.message.guild.id
        
        if guild_id in self.queues:
            self.queues[guild_id].append(source)
        else:
            self.queues[guild_id] = [source]
            
        await ctx.send("Added to queue: %s" % guild_id)
        
        
async def setup(client):
    await client.add_cog(Music(client))