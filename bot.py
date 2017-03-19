import claspbot
from discord.ext import commands
import discord
import logging, sys
import json

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


extensions = [
    "claspbot.trivial",
    "claspbot.event"
]


client = discord.Client()
prefix = ["~"]

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    logger.info("Logged in as:")
    logger.info("Username: {}".format(bot.user.name))
    logger.info("ID: {}".format(bot.user.id))

@bot.command(pass_context=True)
async def hey(ctx):
    msg = ctx.message
    await bot.say("hey {}".format(msg.author.mention))

@bot.event
async def on_message(message):
    await bot.process_commands(message)


def load_credential():
    with open('credentials.json','r') as cred:
        return json.load(cred)


def main():
    cred = load_credential()

    bot.client_id = cred['client_id']
    token = cred['token']

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))


    bot.run(token)


if __name__ == '__main__':
    main()