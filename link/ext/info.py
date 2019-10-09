#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import Optional
import discord
from discord.ext import commands
from tools.paginator import HelpPaginator


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(name="help", aliases=['?', "h"], brief="Shows help")
    async def help(self, ctx: commands.Context, *, cmdname: str = '') -> None:
        """
        Shows the bots help message.
        :param ctx: Some data like the channel or author
        :param cmdname: The name of the command
        :return: Some data like the channel or author
        """
        if cmdname:  # TODO: update help command
            cmd = self.bot.get_command(cmdname)
            msg = f"```py\n{self.bot.command_prefix}[{cmd.name}"
            for alias in cmd.aliases:
                msg += f"|{alias}"

            msg += f"]\n{cmd.help or 'No description provided yet'}\n```"
        else:
            pag: HelpPaginator = HelpPaginator(ctx.channel, self.bot, ctx.author)

            for cog in self.bot.cogs:
                if cog.lower() == 'events':
                    continue

                pag.add_cog_page(cog)

            await pag.start()

    @commands.command(name="user", aliases=["u"], brief="Shows user imformation")
    async def user(self, ctx: commands.Context, *, member: discord.Member = None) -> None:
        """
        Shows common user information.
        :param ctx: Some data like the channel or author
        :param member: The member we are looking for
        :return: There is no return statement
        """

        user: Optional[discord.User, discord.Member] = member or ctx.author

        await ctx.send(embed=self.user_information(user, ctx))
        
    @commands.command(name="me", aliases=[], brief="Shows your user information")
    async def me(self, ctx):
        """
        Shows your user information.
        :param ctx: Some data like the channel or author
        :return: There is no return statement
        """

        user: Optional[discord.User, discord.Member] = ctx.author

        await ctx.send(embed=self.user_information(user, ctx))

    @staticmethod
    def user_information(user, ctx) -> discord.Embed:
        """
        Visualise some user information.
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
    The setup function for the discord.py library.
    :param bot: The bot
    :return: There is no return statement
    """
    bot.add_cog(Info(bot))
