#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''moderation.py:
Commands for moderting users.
'''
###### IMPORTS ######

import discord
from discord.ext import commands

import json


###### MAIN ######

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, user: discord.Member, reas=None):
        await user.kick(reason=reas)
        await ctx.send('{} was kicked by {}!\nReason:```{}```'.format(user.mention, ctx.author, reas))
        
    @commands.command(name='nick')
    @commands.has_permissions(manage_nicknames=True)
    async def _nick(self, ctx, user: discord.Member, *, new: str):
        await user.edit(nick=new)
        await ctx.message.add_reaction(self.bot.reactions['done'])

###### RUN ######

def setup(bot):
    bot.add_cog(Moderation(bot))
