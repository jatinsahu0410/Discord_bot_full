import discord
from discord.ext import commands
import os 
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = commands.Bot(command_prefix = "!", intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status= discord.Status.idle, activity= discord.Activity(type = discord.ActivityType.listening, name="spotify"))
    print("Bot is ready ")
    print("--------------------------------")
    
initail_extension = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initail_extension.append("cogs." + filename[:-3])
        
print(initail_extension)

async def load_extensions():
    for extension in initail_extension:
        await client.load_extension(extension)

if __name__ == "__main__":
    async def main():
        async with client:
            await load_extensions()
            await client.start(os.getenv('TOKEN'))
            
asyncio.run(main())