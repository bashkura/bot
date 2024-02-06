# main.py
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Intents
from discord import member
from dotenv import load_dotenv
import os
from discord import FFmpegPCMAudio


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=('!',), intents=intents)

async def load():
    for filename in os.listdir(os.path.join(os.getcwd(), 'cogs')):
        if filename.endswith('.py'):
            cog = f'cogs.{filename[:-3]}'
            await bot.load_extension(cog)

    
    for extension in bot.extensions:
        bot.add_cog(bot.extensions[extension].setup(bot))



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

async def main():
    await load()
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main function
asyncio.run(main())
