from discord.ext.commands import Bot

with open("token.txt") as fp:
    TOKEN = fp.read().strip()

bot = Bot(command_prefix="-")

if __name__ == '__main__':
    bot.load_extension('commands', )
    bot.load_extension('events')

    bot.run(TOKEN)
