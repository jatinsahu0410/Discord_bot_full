import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        voice.play(source)

client = commands.Bot(command_prefix = "!", intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status= discord.Status.idle, activity= discord.Activity(type = discord.ActivityType.listening, name="spotify"))
    print("Bot is ready ")
    print("--------------------------------")

    
@client.command()
async def hello(ctx):
    await ctx.send("Hello from FUN WITH LOVE Bot")

@client.command()
async def goodbye(ctx):
    await ctx.send("Have a Lovely Day Ahead")
    
@client.event
async def on_member_joined(member):
    channel = client.get_channel(1251586416832544778);
    await channel.send(f'{member} has joined the server')
    
@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        ffmpeg_options = {
            'before_options': '-loglevel debug',  # This will print debug information
            'options': '-vn'
        }
        source = FFmpegPCMAudio("inspire.wav", **ffmpeg_options)
        
        player = PCMVolumeTransformer(source, volume=1.0)
        try:
            voice.play(player)
            await ctx.send("I joined the voice channel and started playing audio.")
            await ctx.send("Finished playing audio.")
        except Exception as e:
            await ctx.send(f"An error occurred while trying to play audio: {str(e)}")
    else:
        await ctx.send("You aren't in a voice channel u have to be in a voice channel to run this command.")
        
@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()    
        await ctx.send("left the channel")
    else:
        await ctx.send("I aim't in a voice channel")
        

@client.command(pass_context = True)
async def pause(ctx):
    voice =  discord.utils.get(client.voice_clients, guild= ctx.guild)
    if voice.is_playing():
        voice.pause()
    else: 
        await ctx.send("I am not playing any audio")
        
@client.command(pass_context = True)
async def resume(ctx):
    voice =  discord.utils.get(client.voice_clients, guild= ctx.guild)
    if voice.is_paused():
        voice.resume()
    else: 
        await ctx.send("I am not playing any audio")
        
@client.command(pass_context = True)
async def stop(ctx):
    voice =  discord.utils.get(client.voice_clients, guild= ctx.guild)
    if voice.is_playing():
        voice.stop()
        await ctx.send("i Stopped the audio")
    else: 
        await ctx.send("I am not playing any audio")
        
@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + ".wav")
    player = PCMVolumeTransformer(source, volume=1.0)
    voice.play(player, after= lambda x = None: check_queue(ctx, ctx.message.guild.id))
    
@client.command(pass_context = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + ".wav"
    source = FFmpegPCMAudio(song)
    
    guild_id = ctx.message.guild.id
    
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]
        
    await ctx.send("Added to queue: %s" % guild_id)
    
abusing_words = ['fuck off', 'idiot', 'dumb', 'losser']

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if any(word in message.content for word in abusing_words):
        await message.delete()
        await message.channel.send("You can't u assuing words in the message")
        
    await client.process_commands(message)
    
@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Dog", url="https://google.com", description="dogs are loyal")
    embed.set_author(name="jatin sahu", url="https://www.youtube.com/watch?v=UoROS78Vtr4&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=9", icon_url="https://cdn.pixabay.com/photo/2024/01/04/16/48/landscape-8487906_1280.jpg")
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2024/01/04/16/48/landscape-8487906_1280.jpg")
    embed.add_field(name="google", value="tech", inline=True)
    await ctx.send(embed = embed)
    
@client.command()
async def message(ctx, user:discord.Member, *, message = None):
    message = "Welcome to the server"
    embed = discord.Embed(title=message)
    await user.send(embed = embed)
    
client.run(os.getenv('TOKEN'))