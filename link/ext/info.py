#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inspect import signature
import datetime
from typing import Optional
import discord
from discord.ext import commands
from tools.paginator import HelpPaginator


class Info(commands.Cog):
    """The info cog"""
    def __init__(self, bot: commands.Bot):
        """The initializer for the Info cog"""
        self.bot: commands.Bot = bot

    @commands.command(name="help", aliases=['?', "h"], brief="Shows help")
    async def help(self, ctx: commands.Context, *, cmdname: str = '') -> None:
        """
        Shows the bots help message.
        :param ctx: Some data like the channel or author
        :param cmdname: The name of the command
        :return: Some data like the channel or author
        """
        if cmdname:
            cmd: commands.Command = self.bot.get_command(cmdname)
            em: discord.Embed = discord.Embed(
                title=f'The {cmd.name} command',
                description=cmd.help.splitlines()[0],
                timestamp=datetime.datetime.utcnow(),
                colour=ctx.author.color
            )
            em.add_field(
                name="Aliases",
                value=f"{'['+'|'.join(cmd.aliases)+']' if cmd.aliases else 'None'}",
                inline=False
            )
            em.add_field(
                name="Signature",
                value=f"{', '.join(list(signature(cmd.callback).parameters)[1:])}",
                inline=False
            )

            em.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

            await ctx.send(embed=em)
        else:
            pag: HelpPaginator = HelpPaginator(ctx.channel, self.bot, ctx.author)

            for cog in self.bot.cogs:
                if not cog.lower() == 'events':
                    pag.add_cog_page(cog)

            await pag.start()

    @commands.command(name="user", aliases=["u"], brief="Shows user imformation")
    async def user(self, ctx: commands.Context, *, member: discord.Member = None) -> None:
        """
        Shows common user information
        :param ctx: Some data like the channel or author
        :param member: The member we are looking for
        :return: There is no return statement
        """

        user: Optional[discord.User, discord.Member] = member or ctx.author

        await ctx.send(embed=self.user_information(user, ctx))
        
    @commands.command(name="me", aliases=[], brief="Shows your user information")
    async def me(self, ctx):
        """
        Shows your user information
        :param ctx: Some data like the channel or author
        :return: There is no return statement
        """

        user: Optional[discord.User, discord.Member] = ctx.author

        await ctx.send(embed=self.user_information(user, ctx))

    @staticmethod
    def user_information(user, ctx) -> discord.Embed:
        """
        Visualise some user information
        :param user: The discord user
        :param ctx: Some data like the channel or author
        :return: The visualised discord embed
        """
        em: discord.Embed = discord.Embed(
            title='Info about {}'.format(user),
            description=user.id,
            timestamp=datetime.datetime.utcnow(),
            colour=user.colour
        )
        em.set_thumbnail(url=user.avatar_url)
        em.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        em.add_field(name='User joined at', value=str(user.joined_at).split('.')[0])
        em.add_field(name='User created at', value=str(user.created_at).split('.')[0])
        em.add_field(name='Time in guild', value=str(datetime.datetime.utcnow() - user.joined_at).split('.')[0])
        em.add_field(name='User is a bot', value=user.bot)

        return em


def setup(bot: commands.Bot) -> None:
    """
    The setup function for the discord.py library
    :param bot: The bot
    :return: There is no return statement
    """
    bot.add_cog(Info(bot))
