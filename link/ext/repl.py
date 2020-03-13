#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import traceback
import inspect
import textwrap
import io
from contextlib import redirect_stdout

from tools import SpecialEmbed, short


class Repl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()
        self.repl_prefix = '.'

    def cleanup_code(self, content):
        """Remove code blocks from the code."""
        
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        content = content.strip(f'{self.repl_prefix} ` \n')

        if content.splitlines()[0].strip() == 'py':
            return content.splitlines()[1:]

    def get_syntax_error(self, e):
        """Get a syntax error."""
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {0}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{type(e).__name__}: {e}```'

    @commands.command(name='exec')
    @commands.is_owner()
    async def _exec(self, ctx, *, body: str):

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

        to_compile = f'async def func():\n{textwrap.indent(body, " "*4)}'  # Todo: Does not work for one-liners

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
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()

            em = SpecialEmbed(
                ctx.guild,
                title='Execution output'
            )

            if value:
                em.add_field(name='Output', value='```py\n' + short(value) + '\n```')

            if ret:
                self._last_result = ret

            if ret is not None:
                ret = str(ret)

                em.add_field(name='Returned', value='```py\n' + short(value) + '\n```')

            await ctx.message.add_reaction(self.bot.done)

            if value and ret is not None:
                await ctx.send(embed=em)

    @commands.command()
    @commands.is_owner()
    async def repl(self, ctx):
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
            return await ctx.send(
                f'Already running a REPL session in this channel. Exit it with `{self.repl_prefix}quit`.'
            )

        self.sessions.add(msg.channel.id)

        await ctx.message.add_reaction(self.bot.done)

        while True:
            response = await self.bot.wait_for('message', check=(
                lambda m: m.author == ctx.author and m.content.startswith(self.repl_prefix)
            ))

            cleaned = self.cleanup_code(response.content)

            if cleaned == 'quit':
                await response.add_reaction(self.bot.done)
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
                fmt = f'{value}{traceback.format_exc()}'
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = f'{value}{result}'
                    variables['_'] = result
                elif value:
                    fmt = value

            try:
                if fmt is not None:
                    await ctx.send('```py\n' + short(fmt) + '\n```')
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send(f'Unexpected error: `{e}`')


def setup(bot):
    bot.add_cog(Repl(bot))
