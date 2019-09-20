from discord.ext import commands


class FunCog(commands.Cog):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")


def setup(bot):
    bot.add_cog(FunCog())