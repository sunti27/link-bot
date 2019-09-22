#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random

import discord
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, config):
        bot_config = config['bot']
        auth = config['auth']

        self.command_prefix = commands.when_mentioned_or(bot_config['command_prefix'])

        bot_config['command_prefix'] = self.command_prefix
        super().__init__(**bot_config)

        with open(auth['token_path']) as token:
            self.__TOKEN = token.read().strip()

        self.client_id = auth['client_id']

        # self.remove_command('help')

    def run(self):
        super().run(self.__TOKEN)

    async def on_connect(self):
        print(f'Trying to connect...')

        await self.change_presence(status=discord.Status.idle)

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')
        print(f'ID: {self.user.id}')

        with open('modules.txt') as modules:
            for module in modules.readlines():
                module = module.strip()
                if not module.startswith('#'):
                    module = module.strip().replace('/', '.')
                    self.load_extension(f'link.ext.{module}')

        self.loop.create_task(self.status_runner())

    async def status_runner(self):
        activities = [
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
                name='your voice'
            ),
            discord.Activity(
                type=discord.ActivityType.streaming,
                name='your data'
            )
        ]

        while True:
            await self.change_presence(status=discord.Status.online, activity=random.choice(activities))

            await asyncio.sleep(60)
