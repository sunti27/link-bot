#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''ext/rextension/rextester.py:
Run 45 programming langauges.
'''

###### IMPORTS ######

import discord
from discord.ext import commands

import aiohttp

from . import api as rxt_api
from . import tools

###### MAIN ######

class RextesterCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        invoke_without_command=True, name='rextester', aliases=['rxt'])
    async def rextester_group(self, ctx, *, source):
        message = []

        code_block = tools.code_block_re.search(source)

        if not code_block or len(code_block.groups()) < 2:
            message.append('```Wrong syntax highlighting!')
            message.append(f'For help type {ctx.prefix}rxt help!```')

            return await ctx.send('\n'.join(message))

        # Extract the code
        language, source = code_block.groups()
        language = language.lower()

        if language not in rxt_api.Language.__members__:
            message.append(f'I don\'t support that language. ({language})')
            message.append(f'For help type {self.bot.command_prefix}rxt help!')

            await ctx.send('\n'.join(message))

        lang_no = rxt_api.Language.__members__[language]

        http = aiohttp.ClientSession()
        response = await rxt_api.execute(http, lang_no, source)

        message.insert(0, '```markdown')

        if response.errors:
            message.append('> ERRORS:')
            message.append(response.errors)

        if response.warnings:
            message.append('> WARNINGS:')
            message.append(response.warnings)

        if response.result:
            message.append('> OUTPUT:')
            message.append(response.result)

        for i in response.stats.split(', '):
            if i.startswith('cpu'):
                message.append(i[0:3].upper() + i[3:])
            else:
                message.append(i[0].upper() + i[1:])
    
        message.append('```')
        await http.close()
        if response.files:
            await ctx.send('\n'.join(message), file=discord.File(*[i for i in response.files]))
        else:
            await ctx.send('\n'.join(message))

    @rextester_group.command()
    async def help(self, ctx):
        """
        Shows all supported languages and their markdown highlighting
        syntax expected to invoke them correctly.
        """
        message = []

        message.append('**Supported languages**')

        for lang in sorted(rxt_api.Language.__members__.keys()):
            lang = lang.lower()
            message.append(f'- {lang.title()} -> `{ctx.prefix}rxt '
                                 f'ˋˋˋ{lang} ...`')
        await ctx.send('\n'.join(message))

###### MAIN ######

def setup(bot):
    bot.add_cog(RextesterCog(bot))
