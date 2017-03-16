from discord.ext import commands
import discord
import logging
import random

from claspbot.utils.number import *

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
        n = parse_int(message)
        if n is not None:
            msg = "You rolled {}".format(random.randint(0, n))
            await self.bot.say(msg)
        else:
            await self.bot.say("Invalid number...Do you know what a number is?")

    @commands.command()
    async def dice(self, message: str):
        msg = message.lower().split(sep='d', maxsplit=1)
        status = True
        print(msg)
        if len(msg)==2:
            n, sides = parse_int(msg[0]), parse_int(msg[1])
            if n is None or sides is None:
                status = False
        else:
            status = False

        if status==True:
            total = sum([random.randint(1,sides) for i in range(n)])
            await self.bot.say("You rolled {}".format(total))
        else:
            await self.bot.say("either that's invalid or I'm dumb FeelsBadMan")

    @commands.command()
    async def avatar(self, user : discord.User):
        await self.bot.say("{}".format(user.avatar_url))


def setup(bot):
    bot.add_cog(Trivial(bot))