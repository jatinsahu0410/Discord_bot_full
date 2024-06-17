import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # for commands in cog : inside of @client u have to write commands
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello from FUN WITH LOVE Bot")
        
    @commands.command()
    async def goodbye(self, ctx):
        await ctx.send("Have a Lovely Day Ahead")
        
    # fo events in cog
    @commands.Cog.listener()
    async def on_member_joined(self, member):
        channel = self.client.get_channel(1251586416832544778);
        await channel.send(f'{member} has joined the server')
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(1251586416832544778);
        await channel.send(f'{member} has left the server')
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.client.user:
            return
        channel = reaction.message.channel
        await channel.send(user.name + " added : " + reaction.emoji)
        
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(user.name + " removed : " + reaction.emoji)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return 
        
        if ("happy" in message.content):
            # emoji can be added by using unicode with `` or directly but the recommeded way is to use unicode \
            emoji = '😊'
            await message.add_reaction(emoji)
            
        await self.client.process_commands(message)
    
async def setup(client):
    await client.add_cog(Greetings(client))
