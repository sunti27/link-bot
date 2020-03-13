#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import inspect
from tools import ContentPaginator


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def src(self, ctx, *, command):
        cmd = self.bot.get_command(command)

        if cmd is None:
            raise discord.ext.commands.errors.CommandNotFound(f'Command "{command}" is not found')

        cmd = inspect.getsource(cmd.callback).splitlines()

        pag = ContentPaginator(ctx.channel, self.bot, ctx.author, f"Source Code for '{command}' command")

        for line in range(len(cmd)-1, 0, -1):
            if cmd[line].strip().startswith('"""') or cmd[line].strip().startswith('async'):
                cmd = '\n'.join(cmd[line+1:])
                break

        pag.paginate(inspect.cleandoc(cmd))

        await pag.start()


def setup(bot):
    bot.add_cog(Owner(bot))
