#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
from datetime import datetime
from discord.ext import commands


class Untis(commands.Cog):
    def __init__(self, bot=None):  # TODO: Finish untis command
        self.bot = bot
        self.LOGIN_ENDPOINT = "https://asopo.webuntis.com/WebUntis/j_spring_security_check"
        self.TIMETABLE_ENDPOINT = "https://asopo.webuntis.com/WebUntis/api/daytimetable/dayLesson?"

    async def get_info(self, day: int = 0):
        async with aiohttp.ClientSession() as session:  #
            await session.post(self.LOGIN_ENDPOINT, data=self.bot._config["untis"])

            now: datetime = datetime.utcnow()

            self.TIMETABLE_ENDPOINT += f"date={now.year}{now.month:0>2}{now.day + day:0>2}&id=4927&type=5"

            response: aiohttp.ClientResponse = await session.get(self.TIMETABLE_ENDPOINT[:-1], allow_redirects=False)

            response.raise_for_status()

            return await response.json()

    @commands.command(name="timetable", aliases=[], brief="")
    async def timetable(self, day: str):
        pass

    @commands.command(name="today", aliases=[], brief="")
    async def timetable_today(self):
        pass


def setup(bot):
    bot.add_cog(Untis(bot))
