# libraries
import os
import random
from urllib.request import urlopen
import json

import discord
import requests
from dotenv import load_dotenv

# bot TOKEN define
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()


def file_to_list(x):
    y = []
    with open(f'{x}' + '.txt') as file:
        for line in file.read().splitlines():
            if not line.startswith('#') and line:
                y.append(line)
    return y


# generate item define
modifiers = file_to_list('modifiers')

nouns = file_to_list('nouns')

owners = file_to_list('owners')

locations = file_to_list('locations')


def generate_item():
    item_name = ""
    option = random.randint(0, 3)
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


# generate location define
def generate_location():
    loc_name = ""
    owner = random.choice(owners)
    location = random.choice(locations)
    modifier = random.choice(modifiers)
    option = random.randint(0, 1)
    match option:
        case 0:
            loc_name = modifier + " " + location
        case 1:
            loc_name = location + " of the " + owner
    return "**" + loc_name + "**"

# generate cta define
def generate_cta():
    res = requests.request('GET', "https://api.thecatapi.com/v1/images/search")
    if (code := res.status_code) == 200:
        cta_link = res.json()[0].get('url')
        return cta_link
    else:
        return f'Error {code}'


# on startup message
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# ping command
@bot.command(description="Pong!")
async def ping(ctx):
    await ctx.respond(f"Pong! {bot.latency}")


# more pls button
class ItemButton(discord.ui.View):
    async def on_timeout(self):
        await self.message.edit(view=None)

    @discord.ui.button(label="more pls", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        await interaction.followup.send(generate_item(), view=ItemButton(timeout=30))


class LocationButton(discord.ui.View):
    async def on_timeout(self):
        await self.message.edit(view=None)

    @discord.ui.button(label="more pls", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        await interaction.followup.send(generate_location(), view=LocationButton(timeout=30))

class CtaButton(discord.ui.View):
    async def on_timeout(self):
        await self.message.edit(view=None)

    @discord.ui.button(label="more pls", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        await interaction.followup.send(generate_cta(), view=CtaButton(timeout=30))


# /cta command
@bot.slash_command(name="cta", description="Send an image of a cta")
async def cta(ctx):
    await ctx.send(generate_cta(), view=CtaButton(timeout=30))



# /item command
@bot.slash_command(name="item", description="Generate a random fantasy item")
async def item(ctx):
    await ctx.respond(generate_item(), view=ItemButton(timeout=30))


# /dungeon command
@bot.slash_command(name="location", description="Generate a random fantasy location")
async def location(ctx):
    await ctx.respond(generate_location(), view=LocationButton(timeout=30))


# /help command
@bot.slash_command(name="help", description="Info about the bot")
async def help(ctx):
    with open('help.txt') as file:
        message = file.read()
    await ctx.respond(message)


# /challenge command
@bot.slash_command(name="challenge", description="Challenge an another user to draw an item!")
async def challenge(ctx, arg1, arg2):
    match arg1:
        case "item":
            await ctx.respond(f" <@{ctx.author.id}> challenges " + arg2 + " to draw " + generate_item() + "!")
        case "location":
            await ctx.respond(f" <@{ctx.author.id}> challenges " + arg2 + " to create " + generate_location() + "!")
        case _:
            await ctx.respond("Invalid arguments! Use /help to see correct syntax.", delete_after=5)


# run the bot
bot.run(TOKEN)
