#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def dice(self, ctx):
        await ctx.send(f'\U0001f3b2 {random.randint(1, 7)}')

    @commands.command()
    async def vap(self, ctx, *, msg):
        result = ''
        for char in msg:
            if char.isspace():
                result += chr(0x3000)
            else:
                result += chr(ord(char) + 0xfee0)
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Fun(bot))
