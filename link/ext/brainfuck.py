#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''brainfuck.py:
Brainfuck interpreter for the bot.
'''

###### IMPORTS ######

import discord
from discord.ext import commands
import asyncio
from io import StringIO
from contextlib import redirect_stdout
import json

from nano.utils import functions


###### MAIN ######

class Brainfuck:
    def __init__(self, bot):
        self.bot = bot

    def exec_bf(self, code, left, right, data, idx):
        '''
        brainfuck interpreter
        src: source string
        left: start index
        right: ending index
        data: input data string
        idx: start-index of input data string
        '''
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
        # tuning machine has infinite array size
        # increase or decrease here accordingly
        arr = [0] * 30000
        ptr = 0
        i = left
        while i <= right:
            s = code[i]
            if s == '>':
                ptr += 1
                # wrap if out of range
                if ptr >= len(arr):
                    ptr = 0
            elif s == '<':
                ptr -= 1
                # wrap if out of range
                if ptr < 0:
                    ptr = len(arr) - 1
            elif s == '+':
                arr[ptr] += 1
            elif s == '-':
                arr[ptr] -= 1
            elif s == '.':
                print(chr(arr[ptr]), end="")
            elif s == ',':
                if idx >= 0 and idx < len(data):
                    arr[ptr] = ord(data[idx])
                    idx += 1
                else:
                    arr[ptr] = 0 # out of input
            elif s =='[':
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

    @commands.command(name='bf', aliases=['brainfuck'])
    async def get_bf(self, ctx, body):
        f = StringIO()
        with redirect_stdout(f):
            self.exec_bf(body, 0, len(body) - 1, "sdfsdf", 0)
        out = functions.paginate(f.getvalue())
        for page in out:
            await ctx.send(page)
        try:
            ctx.message.add_reaction(self.bot.rections['done'])
        except:
            pass

###### RUN ######

def setup(bot):
    bot.add_cog(Brainfuck(bot))
