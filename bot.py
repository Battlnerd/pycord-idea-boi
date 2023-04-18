# libraries
import os
import random
from urllib.request import urlopen
import json

import discord
from dotenv import load_dotenv

# bot TOKEN define
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()

# item command define
modifiers = []
with open('modifiers.txt') as file:
    for line in file.read().splitlines():
        if not line.startswith('#') and line:
            modifiers.append(line)

nouns = []
with open('nouns.txt') as file:
    for line in file.read().splitlines():
        if not line.startswith('#') and line:
            nouns.append(line)

owners = []
with open('owners.txt') as file:
    for line in file.read().splitlines():
        if not line.startswith('#') and line:
            owners.append(line)

options = [0, 1, 2, 3]


def generate_item_name():
    item_name = ""
    option = random.choice(options)
    owner = random.choice(owners)
    noun = random.choice(nouns)
    modifier = random.choice(modifiers)
    match option:
        case 0:
            item_name = modifier + " " + noun
        case 1:
            item_name = noun + " of the " + owner
        case 2:
            item_name = owner + " " + noun
        case 3:
            item_name = noun + " of the " + modifier
    return "**" + item_name + "**"


# cta
def random_cta(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html


# on startup message
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# ping command
@bot.command(description="Pong!")
async def ping(ctx):
    await ctx.respond(f"Pong! {bot.latency}")


# more pls button
class MorePls(discord.ui.View):
    async def on_timeout(self):
        await self.message.edit(view=None)

    @discord.ui.button(label="more pls", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        await interaction.followup.send(generate_item_name(), view=MorePls(timeout=30))


# /item command
@bot.slash_command(name="item", description="Generate a random fantasy item")
async def item(ctx):
    await ctx.respond(generate_item_name(), view=MorePls(timeout=30))


# /help command
@bot.slash_command(name="help", description="Info about the bot")
async def help(ctx):
    with open('help.txt') as file:
        message = file.read()
    await ctx.respond(message)


# /challenge command
@bot.slash_command(name="challenge", description="Challenge an another user to draw an item!")
async def challenge(ctx, arg):
    await ctx.respond(f" <@{ctx.author.id}> challenges " + arg + " to draw " + generate_item_name() + "!")


@bot.slash_command(name="cta", description="Send an image of a cta")
async def cta(ctx):
    cta_link = json.loads(random_cta("https://some-random-api.ml/img/cat"))
    await ctx.respond(cta_link["link"])


# run the bot
bot.run(TOKEN)
