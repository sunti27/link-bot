#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''fun.py:
Funny commands.
'''

###### IMPORTS ######

import discord
from discord.ext import commands

###### MAIN ######

class Fun:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def dice(self, ctx):
        await ctx.send('\U0001f3b2 {}'.format(random.randint(1, 7)))

    @commands.command()
    async def vap(self, ctx, *, msg):
        result = ''
        for char in msg:
            if char.isspace():
                result += chr(0x3000)
            else:
                result += chr(ord(char) + 0xfee0)
        await ctx.send(result)

###### RUN ######

def setup(bot):
    bot.add_cog(Fun(bot))
