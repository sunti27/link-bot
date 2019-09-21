#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from link.engine import Bot


with open("config/discord.json") as fp:
    config = json.load(fp)


bot = Bot(config)


if __name__ == '__main__':
    bot.run()
