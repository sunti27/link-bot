#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, NoReturn, Any, Optional
from discord import Embed, TextChannel, User
from discord.ext.commands import Bot
import datetime


class Paginator:
    def __init__(self, channel: TextChannel, bot: Bot, author: User, content_type: str) -> NoReturn:
        self._pages: List[Optional[Embed, str]] = []
        self._index: int = 0
        self._channel: TextChannel = channel

        self._reactions: Dict[str, Any] = {
            '\u23EA': self.first,
            '\u25C0': self.prev,
            '\u23F9': self.stop,
            '\u25B6': self.next,
            '\u23E9': self.last
        }

        self._msg = None
        self._bot = bot
        self._author = author
        self._type = content_type.lower()

    async def first(self) -> NoReturn:
        self._index = 0

    async def last(self) -> NoReturn:
        self._index = len(self._pages) - 1

    async def next(self) -> NoReturn:
        if not self._index + 1 >= len(self._pages):
            self._index += 1

    async def prev(self) -> NoReturn:
        if not self._index - 1 < 0:
            self._index -= 1

    async def stop(self) -> NoReturn:
        if self._msg:
            await self._msg.clear_reactions()

    async def start(self) -> NoReturn:
        self._msg = await self._channel.send(embed=self._pages[0])

        for reaction in list(self._reactions.keys()):
            await self._msg.add_reaction(reaction)

        self._bot.loop.create_task(self.reaction_updater())

    async def reaction_updater(self) -> None:
        while True:
            reaction, user = await self._bot.wait_for('reaction_add', check=(
                lambda r, u: u == self._author and r.emoji in self._reactions.keys()
            ))

            await self._msg.remove_reaction(reaction, user)

            old_index: int = self._index

            await self._reactions[reaction.emoji]()

            if old_index != self._index:
                if self._type == "embed":
                    await self._msg.edit(embed=self._pages[self._index])


class HelpPaginator(Paginator):
    def __init__(self, channel: TextChannel, bot: Bot, author: User) -> NoReturn:
        super().__init__(channel, bot, author, "embed")

    def add_cog_page(self, cog: str) -> NoReturn:
        cog = self._bot.get_cog(cog)

        em: Embed = Embed(
            title=f'{cog.qualified_name} commands',
            timestamp=datetime.datetime.utcnow(),
            colour=self._author.color
        )

        for cmd in cog.get_commands():
            em.add_field(
                name=f'{self._bot.command_prefix}[{cmd.name}{"|" if cmd.aliases else ""}{"|".join(cmd.aliases)}]',
                value=cmd.brief or 'None',
                inline=False
            )

        em.set_footer(text=self._channel.guild.name, icon_url=self._channel.guild.icon_url)

        self._pages.append(em)