import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.abusing_words = ['fuck off', 'idiot', 'dumb', 'losser']
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return 
        if any(word in message.context for word in self.abusing_words):
            await message.delete()
            await message.channel.send("You can't u assuing words in the message")
            
        await self.client.process_commands(message)
        
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title="Dog", url="https://google.com", description="dogs are loyal")
        embed.set_author(name="jatin sahu", url="https://www.youtube.com/watch?v=UoROS78Vtr4&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=9", icon_url="https://cdn.pixabay.com/photo/2024/01/04/16/48/landscape-8487906_1280.jpg")
        embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2024/01/04/16/48/landscape-8487906_1280.jpg")
        embed.add_field(name="google", value="tech", inline=True)
        await ctx.send(embed = embed)
        
    @commands.command()
    async def message(self, ctx, user:discord.Member, *, message = None):
        message = "Welcome to the server"
        embed = discord.Embed(title=message)
        await user.send(embed = embed)
        
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)
    async def addRole(self, ctx, user : discord.Member, *, role : discord.Role):
        if role in user.roles:
            await ctx.send(f"{user.mention} already has {role.mention}")
        else:
            await user.add_roles(role)
            await ctx.send(f"{user.mention} has been given {role.mention}")
            
    @addRole.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to run this command")
            
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)
    async def removeRole(self, ctx, user : discord.Member, *, role : discord.Role):
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f"{user.mention} role removed successfully to {role.name}")
        else:
            await ctx.send(f"{user.mention} does not have the role {role.name}")
            
    @addRole.error
    async def removeRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to run this command")

async def setup(client):
    await client.add_cog(Admin(client))
        