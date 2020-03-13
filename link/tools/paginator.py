#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, NoReturn, Any, Optional
from discord import TextChannel, User
from . import RawEmbed
from discord.ext.commands import Bot
import datetime


class Paginator:
    def __init__(self, channel: TextChannel, bot: Bot, author: User) -> NoReturn:
        self.pages: List[Optional[RawEmbed, str]] = []
        self.index: int = 0
        self.channel: TextChannel = channel

        self.reactions: Dict[str, Any] = {
            '\u23EA': self.first,
            '\u25C0': self.prev,
            '\u23F9': self.stop,
            '\u25B6': self.next,
            '\u23E9': self.last
        }

        self.msg = None
        self.bot = bot
        self.author = author

    async def first(self) -> NoReturn:
        self.index = 0

    async def last(self) -> NoReturn:
        self.index = len(self.pages) - 1

    async def next(self) -> NoReturn:
        if not self.index + 1 >= len(self.pages):
            self.index += 1

    async def prev(self) -> NoReturn:
        if not self.index - 1 < 0:
            self.index -= 1

    async def stop(self) -> NoReturn:
        if self.msg:
            await self.msg.clear_reactions()

    async def start(self) -> NoReturn:
        for idx in range(len(self.pages)):
            self.pages[idx].set_footer(
                text=f'Page [{idx+1}/{len(self.pages)}]',
                icon_url=self.channel.guild.icon_url
            )

        self.msg = await self.channel.send(embed=self.pages[0])

        if len(self.pages) > 1:
            for reaction in list(self.reactions.keys()):
                await self.msg.add_reaction(reaction)

            self.bot.loop.create_task(self.reaction_updater())

    async def reaction_updater(self) -> None:
        while True:
            reaction, user = await self.bot.wait_for('reaction_add', check=(
                lambda r, u: u == self.author and r.emoji in self.reactions.keys()
            ))

            await self.msg.remove_reaction(reaction, user)

            old_index: int = self.index

            await self.reactions[reaction.emoji]()

            if old_index != self.index:
                await self.msg.edit(embed=self.pages[self.index])


class HelpPaginator(Paginator):
    def __init__(self, channel: TextChannel, bot: Bot, author: User) -> NoReturn:
        super().__init__(channel, bot, author)

    def add_cog_page(self, cog: str) -> NoReturn:
        cog = self.bot.get_cog(cog)

        em: RawEmbed = RawEmbed(
            title=f'{cog.qualified_name} commands',
            timestamp=datetime.datetime.utcnow(),
            colour=self.author.color
        )

        for cmd in cog.get_commands():
            em.add_field(
                name=f'{self.bot.command_prefix}[{cmd.name}{"|" if cmd.aliases else ""}{"|".join(cmd.aliases)}]',
                value=cmd.brief or 'None'
            )

        self.pages.append(em)


class ContentPaginator(Paginator):
    def __init__(self, channel: TextChannel, bot: Bot, author: User, headline: str) -> NoReturn:
        super().__init__(channel, bot, author)

        self.headline = headline

    def _add_text_page(self, content):
        em: RawEmbed = RawEmbed(
            title=self.headline,
            timestamp=datetime.datetime.utcnow(),
            colour=self.author.color,
            description=content
        )

        self.pages.append(em)

    def paginate(self, text: str):
        step = 2030

        text = text.replace('```', '\u02cb'*3)

        for c in range(0, len(text), step):
            self._add_text_page('```py\n' + text[c*step:(c+1)*step] + '\n```')  # TODO: src > 2000 does not work


def short(text: str):
    text = text.replace('```', '\u02cb'*3)

    return (text[:1000] + '\n...') if len(text) > 1000 else text
