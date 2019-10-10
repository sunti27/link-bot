#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', aliases=[], brief="Kicks a member")
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str = ""):
        """
        Kick a member from the current guild.
        :param ctx: Some data like the channel or author
        :param user: The user who will be kicked
        :param reason: The reason for kicking the user
        :return: There is no return statement
        """

        await user.kick(reason=reason)

        em: discord.Embed = discord.Embed(
            title='{} has been kicked'.format(user),
            description=reason,
            timestamp=datetime.datetime.utcnow(),
            colour=user.colour,
        )
        em.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=em)
        
    @commands.command(name='nick', aliases=[], brief="Changes nickname")
    async def nick(self, ctx, user: discord.Member, *, new: str):
        """
        Change a members name
        :param ctx: Some data like the channel or author
        :param user: The user who's nickname will be changed
        :param new: The new nickname
        :return: There is no return statement
        """
        await user.edit(nick=new)
        await ctx.message.add_reaction("\u2705")


def setup(bot):
    bot.add_cog(Moderation(bot))
