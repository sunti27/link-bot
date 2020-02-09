#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import json
import inspect

from tools import ContentPaginator


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_owner(self, user):
        if user.id == json.load(open('setup/config'))['owner']['owner_id']:
            return True
        return False

    @commands.command()
    @commands.is_owner()
    async def src(self, ctx, *, command):
        cmd = inspect.getsource(self.bot.get_command(command).callback)
        for page in [cmd]:
            await ctx.send(page)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send('```Logged out!```')
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))
