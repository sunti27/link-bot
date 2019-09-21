#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''ext/info.py:
Commands to get information about something.
'''

###### IMPORTS ######

import discord
from discord.ext import commands
from io import StringIO
from contextlib import redirect_stdout
import json
import datetime

from nano.utils import functions

###### MAIN ######

class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *, cmd = None):
        msg = """**Nano help message:**
```py
Fun:              # fun commands
  vap             <text>``````Useful:           # useful commands
  ping             
  purge           [limit]      
    [-u|--user]   <user> [limit]
    [-b|--bot]    [limit]         
    [-w|--word]   <word> [limit]``````Moderation:       # commands for moderation
  kick            <user> [reason] 
  nick            <user> <new>``````Info:             # commands to get info
  user            <user>
  me 
  help            [command]``````Compiler:         # public execute commands
  [rxt|rextester] <source>
  [bf|brainfuck]  <source>``````REPL:             # executing commands for owner
  exec            <code>
  repl            # prefix = %``````
Owner:            # commands for owner
  src             <command>
  shutdown
```"""
        msg += '```' + ''.join([
            'For more help on a command type ',
            f'{ctx.prefix}help <command>.\n',
            'For help on reactions type ',
            f'{ctx.prefix}help reactions.'
        ]) + '```'
        
        await ctx.send(msg)
        
    @commands.command()
    async def user(self, ctx, member: discord.Member = None):
        user = member or ctx.author
        em = discord.Embed(
            title='Info about {}'.format(user),
            description=user.id,
            timestamp=datetime.datetime.utcnow(),
            colour=user.top_role.colour
        )
        em.set_thumbnail(url=user.avatar_url)
        em.set_footer(
                text=ctx.guild.name, 
                icon_url=ctx.guild.icon_url
                )
        em.add_field(
                name='User joined at', 
                value=str(user.joined_at).split('.')[0]
                )
        em.add_field(
                name='User created at', 
                value=str(user.created_at).split('.')[0]
                )
        em.add_field(
                name='Time in guild', 
                value=str(
                    datetime.datetime.utcnow()-user.joined_at
                    ).split('.')[0]
                  )
        em.add_field(name='User is a bot', value=user.bot)
        await ctx.send(embed=em)
        
    @commands.command()
    async def me(self, ctx):
        user = ctx.author
        em = discord.Embed(
            title='Info about {}'.format(user),
            description=user.id,
            timestamp=datetime.datetime.utcnow(),
            colour=user.top_role.colour
        )
        em.set_thumbnail(url=user.avatar_url)
        em.set_footer(
                text=ctx.guild.name, 
                icon_url=ctx.guild.icon_url
                )
        em.add_field(
                name='You joined at', 
                value=str(user.joined_at).split('.')[0]
                )
        em.add_field(
                name='Your account created at', 
                value=str(user.created_at).split('.')[0]
                )
        em.add_field(
                name='Time in guild', 
                value=str(
                    datetime.datetime.utcnow()-user.joined_at
                    ).split('.')[0]
                )
        em.add_field(name='You are a bot', value=user.bot)
        await ctx.send(embed=em)
        
###### RUN ######

def setup(bot):
    bot.add_cog(Info(bot))
