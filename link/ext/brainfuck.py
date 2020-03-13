#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
from tools import ContentPaginator


class Brainfuck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bf', aliases=['brainfuck'])
    async def get_bf(self, ctx, code):
        output = ''

        left = 0
        right = len(code) - 1
        idx = 0
        data = 'sdfsdf'

        if len(code) == 0:
            return
        if left < 0:
            left = 0
        if left >= len(code):
            left = len(code) - 1
        if right < 0:
            right = 0
        if right >= len(code):
            right = len(code) - 1

        arr = [0] * 30000
        ptr = 0
        i = left
        while i <= right:
            s = code[i]
            if s == '>':
                ptr += 1

                if ptr >= len(arr):
                    ptr = 0
            elif s == '<':
                ptr -= 1

                if ptr < 0:
                    ptr = len(arr) - 1
            elif s == '+':
                arr[ptr] += 1
            elif s == '-':
                arr[ptr] -= 1
            elif s == '.':
                output += chr(arr[ptr])
            elif s == ',':
                if 0 <= idx < len(data):
                    arr[ptr] = ord(data[idx])
                    idx += 1
                else:
                    arr[ptr] = 0
            elif s == '[':
                if arr[ptr] == 0:
                    loop = 1
                    while loop > 0:
                        i += 1
                        c = code[i]
                        if c == '[':
                            loop += 1
                        elif c == ']':
                            loop -= 1
            elif s == ']':
                loop = 1
                while loop > 0:
                    i -= 1
                    c = code[i]
                    if c == '[':
                        loop -= 1
                    elif c == ']':
                        loop += 1
                i -= 1
            i += 1

        pag = ContentPaginator(ctx.channel, self.bot, ctx.author, 'Brainfuck output')

        pag.paginate(output)

        await pag.start()

        await ctx.message.add_reaction(self.bot.done)


def setup(bot):
    bot.add_cog(Brainfuck(bot))
