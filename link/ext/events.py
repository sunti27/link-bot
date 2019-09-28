#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import discord
from discord.ext import commands
import asyncio


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #    self.lfe = bot.reactions['look_for_error']

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if 'Forbidden' in str(error):
    #         return await ctx.message.add_reaction(':x:')
    #     await ctx.message.add_reaction(self.bot.reactions['error'])
    #     await ctx.message.add_reaction(self.lfe)
    #     reaction = await self.bot.wait_for(
    #         'reaction_add', check=(
    #             lambda r, u: u == ctx.author and r.emoji == self.lfe
    #             )
    #     )
    #     await ctx.channel.send('```{}```'.format(error))
    #     await ctx.message.remove_reaction(self.lfe, ctx.author)

    # @commands.Cog.listener()
    # async def on_message_edit(self, before, after):
    #     if after.content.startswith(self.bot.command_prefix):
    #         try:
    #             await self.bot.process_commands(after)
    #         except:
    #             pass
    #         else:
    #             await asyncio.sleep(0.5)
    #             await after.remove_reaction(self.bot.reactions['error'], after.guild.me)
    #             await after.remove_reaction(self.lfe, after.guild.me)
    #             await asyncio.sleep(0.5)


#    async def on_member_join(self, user: discord.Member):
#        em = discord.Embed(description = 'Welcome {}'.format(user), timestap = datetime.datetime.utcnow(), color = discord.Colour.teal())
#        em.set_footer(text = 'User joined')
#        await user.guild.system_channel.send(embed = em)

#    async def on_member_remove(self, user: discord.Member):
#        em = discord.Embed(description = 'RIP {}'.format(user), timestap = datetime.datetime.utcnow(), color = discord.Colour.red())
#        em.set_footer(text = 'User left')
#        await user.guild.system_channel.send(embed = em)


def setup(bot):
    bot.add_cog(Events(bot))
