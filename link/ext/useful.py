#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import time
import asyncio


class Useful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases=["p"], brief="Show bot latency")
    async def ping(self, ctx):
        """
        This command displays the time it takes the bot to answer.
        :param ctx:
        :return:
        """
        before = time.monotonic()
        await (await self.bot.ws.ping())
        after = time.monotonic()
        delta = (after - before) * 1000
        await ctx.send('Pong \U0001f3d3, took {0:.1f}ms!'.format(delta))

    @commands.group(invoke_without_command=True, name="purge", aliases=['del', 'rm'], brief="Deletes messages")
    async def purge(self, ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount+1)
        msg = await ctx.send('Deleted {} message(s)!'.format(len(list(deleted))))
        await asyncio.sleep(2)
        await msg.delete()

    @purge.command(name='word', aliases=['w'], brief="Deletes messages that contain a word")
    async def purge_word(self, ctx, word: str, amount: int = 10):
        deleted = await ctx.channel.purge(limit=amount, check=(lambda m: word in m.content))

        len_del = len(list(deleted))

        msg = await ctx.send(
            f'Deleted {len_del} message{"s" if len_del > 1 else ""} that contain{"s" if len_del > 1 else ""} "{word}"!'
        )

        await asyncio.sleep(2)
        await msg.delete()

        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass

    @purge.command(name='user', aliases=['u'], brief="Delete messages of a user")
    async def purge_user(self, ctx, user: discord.Member, amount: int = 10):
        deleted = await ctx.channel.purge(limit=amount, check=(lambda m: m.author == user))
        len_del = len(list(deleted))

        msg = await ctx.send(f'Deleted {len_del} message{"s" if len_del > 1 else ""} of {user}!')

        await asyncio.sleep(2)
        await msg.delete()

        try:
            await ctx.message.delete()
        except discord.Errors.NotFound:
            pass

    @purge.command(name='bot', aliases=['b'])
    async def purge_bot(self, ctx, amount: int = 10):
        deleted = await ctx.channel.purge(limit=amount, check=(lambda m: m.author.bot))
        msg = await ctx.send(f'Deleted {len(list(deleted))} bot message{"s" if len(list(deleted)) > 1 else ""}!')

        await asyncio.sleep(2)
        await msg.delete()
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Useful(bot))
