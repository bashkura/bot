import discord
from discord.ext import commands
from difflib import get_close_matches
import json
from discord import Intents  
from dotenv import load_dotenv
import os
from discord.ext.commands import has_permissions, MissingPermissions
from discord import member
from typing import Final
import requests

class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1203382951287726203)
        await channel.send('Hello')


    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = self.bot.get_channel(1203382951287726203)
        await channel.send('goodbye')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel

        # Check if the reaction is a thumbs up emoji
        if str(reaction.emoji) == "👍":
            await channel.send(f"Thanks for the thumbs up, {user.mention}!")

        # Check if the reaction is a thumbs down emoji
        elif str(reaction.emoji) == "👎":
            await channel.send(f"Sorry to hear that, {user.mention}.")

        


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if ("happy") in message.content:
            emoji = "😃"
            await message.add_reaction(emoji)

        if ("დამპალო") in message.content:
            member = message.author
            await message.channel.send(f'{member.mention}, you were kicked for using inappropriate language.')
            await member.kick(reason='Inappropriate language')

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'User {member} has been kicked.')
        except discord.Forbidden:
            await ctx.send("I do not have permission to kick this user.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred: {e}")


        



async def setup(bot):
    await bot.add_cog(Greetings(bot))