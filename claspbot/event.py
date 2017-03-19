from discord.ext import commands
from claspbot.utils.number import *
import discord


logger = logging.getLogger('discord')


class Event:
    # TODO: handle 0-based indexing more elegantly
    # TODO: refactor creation of server.channel id
    # TODO: refactor check of running vote
    def __init__(self, bot):
        logger.info("Loaded extension: {}".format(self.__class__.__name__))
        self.bot = bot
        self.vote = {}

    @commands.command(pass_context=True)
    async def voting(self, ctx, *, message):
        channel = ctx.message.channel
        server = ctx.message.server
        id = "{}.{}".format(server, channel)

        items = message.split(",")
        if len(items) <= 1:
            await self.bot.say("you can't have only one item in voting")
        else:
            self.vote[id] = Vote(items)
            await self.bot.say(self.vote[id].result)

    @commands.command(pass_context=True)
    async def v(self, ctx, message : str):
        channel = ctx.message.channel
        server = ctx.message.server
        id = "{}.{}".format(server, channel)

        if id not in self.vote:
            await self.bot.say("no running vote on this channel")
            return

        num = parse_int(message)
        if num is None:
            await self.bot.say("invalid vote")
            return

        try:
            self.vote[id].insert_vote(num-1, ctx.message.author)
        except IndexError as ie:
            await self.bot.say("invalid vote")

    @commands.command(pass_context=True)
    async def endvote(self, ctx):
        channel = ctx.message.channel
        server = ctx.message.server
        id = "{}.{}".format(server, channel)

        if id not in self.vote:
            await self.bot.say("no running vote on this channel")
            return

        await self.bot.say(self.vote[id].result)

        self.vote[id].destroy_vote()
        self.vote.pop(id, None)



class Vote:
    """
    assuming the voting wont be abused by having crazy amount of vote items
    1 voting per channel??
    """
    def __init__(self, vote_items):
        self.vote_index = {k:v for k,v in enumerate(vote_items)}
        self.voters = {keys:[] for keys in self.vote_index}
        self.voted_by_user = {}

    def insert_vote(self, item_number, voter : discord.User):
        """

        :param item_number:
        :param voter:
        :return: raise IndexError if invalid index
        """
        # invalid vote
        if item_number >= len(self.voters) or item_number < 0:
            raise IndexError
            return

        # if user already voted, remove current vote
        if voter.id in self.voted_by_user:
            if item_number == self.voted_by_user[voter.id]:
                return # if same vote then do nothing
            else:
                key = self.voted_by_user[voter.id]
                self.voters[key].remove(voter.id)

        # insert new vote
        if voter.id not in self.voters[item_number]:
            self.voters[item_number].append(voter.id)
            self.voted_by_user[voter.id] = item_number

    def count_vote(self):
        vote_count = [[self.vote_index[k],len(self.voters[k])] for k in self.voters]
            #.sort(key=lambda x:x[1], reverse=True)
        return vote_count

    def destroy_vote(self):
        self.vote_items = None
        self.vote_index = None
        self.voters = None
        self.voted_by_user = None

    def show_vote_items(self):
        return list(self.voters.items())

    @property
    def result(self):
        # TODO: format result better
        msg = []
        for idx, item in enumerate(self.count_vote()):
            item_name, count = item
            msg.append("{}. {}: {}".format(idx+1, item_name, count))
        return "\n".join(msg)

def setup(bot):
    bot.add_cog(Event(bot))