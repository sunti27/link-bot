#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import discord
from discord.ext import commands
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from tools import Embed


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self._reactions: Dict[str, Any] = {
            'forbidden': '\U0001F6AB',
            'error_lookup': '\u2753'
        }
        self._last_error_msg: Optional[discord.Message, None] = None  # TODO: UPGRADE

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if 'Forbidden' in str(error):
            return await ctx.message.add_reaction(self._reactions['forbidden'])

        await ctx.message.add_reaction(self._reactions['error_lookup'])

        await self.bot.wait_for(
            'reaction_add', check=(
                lambda r, u: u == ctx.author and r.emoji == self._reactions['error_lookup']
                )
        )
        self._last_error_msg = await ctx.channel.send('```{}```'.format(error))
        await ctx.message.remove_reaction(self._reactions['error_lookup'], ctx.author)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.content.startswith(self.bot.command_prefix):
            await self.bot.process_commands(after)

            await asyncio.sleep(0.5)

            await self._last_error_msg.delete()
            await after.remove_reaction(self._reactions['error_lookup'], before.guild.me)

    @commands.Cog.listener()
    async def on_member_join(self, user: discord.Member) -> None:
        em: Embed = Embed(
            title="User joined!",
            description='Welcome {}'.format(user),
            timestap=datetime.utcnow(),
            color=discord.Colour.teal()
        )

        em.set_thumbnail(url=user.avatar_url)

        await user.guild.system_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, user: discord.Member) -> None:
        em: Embed = Embed(
            title="User left!",
            description='RIP {}'.format(user),
            timestamp=datetime.utcnow(),
            color=discord.Colour.red()
        )

        em.set_thumbnail(url=user.avatar_url)

        await user.guild.system_channel.send(embed=em)


def setup(bot):
    bot.add_cog(Events(bot))
