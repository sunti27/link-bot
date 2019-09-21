#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''ext/useful.py:
Useful commands.
'''

###### IMPORTS ######

import discord
from discord.ext import commands

import time
import asyncio 

###### MAIN ######

class Useful:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        before = time.monotonic()
        await (await self.bot.ws.ping())
        after = time.monotonic()
        tim = (after - before) * 1000
        await ctx.send('Pong \U0001f3d3, took {0:.1f}ms!'.format(tim))

    @commands.group(invoke_without_command=True)
    async def purge(self, ctx, lim: int):
        deleted = await ctx.channel.purge(limit=lim)
        msg = await ctx.send('Deleted {} message(s)!'.format(len(list(deleted))))
        await asyncio.sleep(1)
        await msg.delete()

    @purge.command(name='-w', aliases=['--word'])
    async def purge_word(self, ctx, word: str, lim: int = 10):
        deleted = await ctx.channel.purge(limit=lim, check=(lambda m: word in m.content))
        msg = await ctx.send('Deleted {} message(s) that contains "{}"!'.format(len(list(deleted)), word))
        await asyncio.sleep(1)
        await msg.delete()
        await asyncio.sleep(1)
        try:
            await ctx.message.delete()
        except:
            pass

    @purge.command(name='-u', aliases=['--user'])
    async def purge_user(self, ctx, user: discord.Member, lim: int = 10):
        deleted = await ctx.channel.purge(limit = lim, check = (lambda m: m.author == user))
        msg = await ctx.send('Deleted {} message(s) of {}!'.format(len(list(deleted)), user))
        await asyncio.sleep(1)
        await msg.delete()
        await asyncio.sleep(1)
        try:
            await ctx.message.delete()
        except:
            pass

    @purge.command(name='-b', aliases=['--bot'])
    async def purge_bot(self, ctx, lim: int = 10):
        deleted = await ctx.channel.purge(limit=lim, check=(lambda m: m.author.bot))
        msg = await ctx.send('Deleted {} bot message(s)!'.format(len(list(deleted))))
        await asyncio.sleep(1)
        await msg.delete()
        await asyncio.sleep(1)
        await ctx.message.delete()

###### RUN ######

def setup(bot):
    bot.add_cog(Useful(bot))