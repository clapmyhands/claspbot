import discord
import logging
import random

import claspbot.utils.number as number

from discord.ext import commands

logger = logging.getLogger('discord')


class Trivial:
    """
    handle trivial commands
    """
    def __init__(self, bot):
        logger.info("Loaded extension: {}".format(self.__class__.__name__))
        self.bot = bot

    @commands.command()
    async def roll(self, message: str):
        n = number.parse_int(message)
        if n is not None:
            msg = "You rolled {}".format(random.randint(0, n))
            await self.bot.say(msg)
        else:
            await self.bot.say("Invalid number...")

    @commands.command()
    async def dice(self, message: str):
        msg = message.lower().split(sep='d', maxsplit=1)
        status = True
        print(msg)
        if len(msg) == 2:
            n, sides = number.parse_int(msg[0]), number.parse_int(msg[1])
            if n is None or sides is None:
                status = False
        else:
            status = False

        if status is True:
            total = sum([random.randint(1, sides) for i in range(n)])
            await self.bot.say("You rolled {}".format(total))
        else:
            await self.bot.say("either that's invalid or I'm dumb FeelsBadMan")

    @commands.command()
    async def avatar(self, user: discord.User):
        await self.bot.say("{}".format(user.avatar_url))


def setup(bot):
    bot.add_cog(Trivial(bot))
