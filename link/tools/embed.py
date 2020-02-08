import discord


class Embed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_field(self, *args, **kwargs):
        super().add_field(*args, **kwargs, inline=False)
