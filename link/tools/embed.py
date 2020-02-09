import discord
from datetime import datetime


class RawEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_field(self, **kwargs):
        kwargs.pop('inline', {})

        super().add_field(inline=False, **kwargs)


class SpecialEmbed(RawEmbed):
    def __init__(self, guild, **kwargs):
        kwargs.pop('timestamp', {})

        super().__init__(timestamp=datetime.utcnow(), **kwargs)

        self.set_footer(text=guild.name, icon_url=guild.icon_url)
