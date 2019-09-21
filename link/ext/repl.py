#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''ext/repl.py:
Here are repl commands for the bot.
'''

###### IMPORTS ######

import discord
from discord.ext import commands

import time
import datetime
import os
import sys
import random
import math
import asyncio
import traceback
import inspect
import textwrap
import io
import json
from contextlib import redirect_stdout

from nano.utils import functions


###### MAIN ######

class Repl:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()
        self.repl_prefix = '%'

    def cleanup_code(self, content):
        '''Remove code blocks from the code.'''
        
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip(f'{self.repl_prefix} ` \n')

    def get_syntax_error(self, e):
        '''Get a syntax error.'''
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.command(name='exec')
    async def _exec(self, ctx, *, body: str):
        if ctx.author.id != json.load(
                open('setup/config.json')
            )['owner']['owner_id']:
        	return await ctx.message.add_reaction(self.bot.reactions['not_allowed'])

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n{}'.format(textwrap.indent(body, '  '))

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send('```py\n{}{}\n```'.format(value, traceback.format_exc()))
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction(self.bot.reactions['done'])
            except:
                pass
            
            value = stdout.getvalue()
            output = []
            
            if value:
                output.append('# Output: ')
                if len(value.split('\n')) > 2:
                    output[0] += f'\n{value}'
                else:
                    output[0] += value
            
            if ret:
                output.append('# Returned: {}'.format(ret))
                self._last_result = ret
            
            if output:
                for page in functions.paginate('\n'.join(output)):
                    await ctx.send(page)

    @commands.command()
    async def repl(self, ctx):
        if ctx.author.id != json.load(
                open('setup/config.json')
            )['owner']['owner_id']:
        	return await ctx.message.add_reaction(self.bot.reactions['not_allowed'])

        msg = ctx.message

        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'guild': msg.guild,
            'channel': msg.channel,
            'author': msg.author,
            '_': None,
        }

        if msg.channel.id in self.sessions:
            return await ctx.send('Already running a REPL session in this channel. Exit it with `{}quit`.'.format(self.repl_prefix))


        self.sessions.add(msg.channel.id)
        await ctx.message.add_reaction(self.bot.reactions['done'])
        while True:
            response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.content.startswith(self.repl_prefix))

            cleaned = self.cleanup_code(response.content)

            if cleaned == 'quit':
                await response.add_reaction(self.bot.reactions['done'])
                return self.sessions.remove(msg.channel.id)

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = '{}{}'.format(value, traceback.format_exc())
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = '{}{}'.format(value, result)
                    variables['_'] = result
                elif value:
                    fmt = '{}'.format(value)

            try:
                if fmt is not None:
                    for page in functions.paginate(fmt):
                        await ctx.send(page)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send('Unexpected error: `{}`'.format(e))

###### RUN ######

def setup(bot):
    bot.add_cog(Repl(bot))
