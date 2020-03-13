#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
import json
from typing import List, Dict, Optional, NoReturn
import discord
from discord.ext import commands


class Bot(commands.Bot):
    """The bots class"""
    def __init__(self) -> NoReturn:
        """Initializer for the bot class"""
        with open("config.json") as config:
            self._config: Dict[str, Optional[str, int]] = json.load(config)

        super().__init__(
            command_prefix=self._config["bot"]["command_prefix"],
            description=self._config["bot"]["description"]
        )

        self.owner: Optional[discord.User, None] = None
        self.remove_command('help')

        self.done = '\u2705'

    def run(self) -> NoReturn:
        """The improved run method"""
        super().run(self._config["auth"]["token"])

    async def on_connect(self) -> NoReturn:
        """Event that is called on connection"""
        print('Trying to connect...')

        await self.change_presence(status=discord.Status.idle)

    async def on_ready(self) -> NoReturn:
        """Event that is called when the bot is ready"""
        self.owner = (await self.application_info()).owner

        print(f'Logged in as {self.user.name}')
        print(f'ID: {self.user.id}')
        print(f'Owner: {self.owner}')

        with open('../modules.txt') as modules:
            for module in modules.readlines():
                module = module.strip()
                if not module.startswith('#') and module:
                    module = module.strip().replace('/', '.')
                    self.load_extension(f'link.ext.{module}')

        self.loop.create_task(self.status_runner())

    async def status_runner(self) -> NoReturn:
        """Background task that changes bots activity"""
        activities: List[discord.Activity] = [
            discord.Activity(
                type=discord.ActivityType.playing,
                name='with your data'
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name='y\'all'
            ),
            discord.Activity(
                type=discord.ActivityType.listening,
                name='your conversations'
            ),
            discord.Activity(
                type=discord.ActivityType.streaming,
                name='your data'
            )
        ]

        while True:
            await self.change_presence(status=discord.Status.online, activity=random.choice(activities))

            await asyncio.sleep(60)
