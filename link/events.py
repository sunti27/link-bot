from textwrap import dedent

from discord.ext import commands


class MainEventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def start(self):
        owner = (await self.bot.application_info()).owner

        print(dedent(
            f"""
            I'm ready to go!
            Logged in as: {self.bot.user}
            User ID: {self.bot.user.id}
            Owner: {owner}
            """
        ))


def setup(bot):
    bot.add_cog(MainEventCog(bot))
