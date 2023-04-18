import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()

# item command define
with open('modifiers.txt') as file:
    modifiers = file.read().splitlines()

with open('nouns.txt') as file:
    nouns = file.read().splitlines()

with open('owners.txt') as file:
    owners = file.read().splitlines()

options = [0, 1, 2]


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
    return "**" + item_name + "**"


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.command(description="Pong!")
async def ping(ctx):
    await ctx.respond(f"Pong! {bot.latency}")


class MorePls(discord.ui.View):
    async def on_timeout(self):
        await self.message.edit(view=None)

    @discord.ui.button(label="more pls", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=None)
        await interaction.followup.send(generate_item_name(), view=MorePls(timeout=30))


@bot.slash_command(name="item", description="Generate a random fantasy item")
async def item(ctx):
    await ctx.respond(generate_item_name(), view=MorePls(timeout=30))


@bot.slash_command(name="help", description="Info about the bot")
async def help(ctx):
    with open('help.txt') as file:
        message = file.read()
    await ctx.respond(message)


@bot.slash_command(name="challenge", description="Challenge an another user to draw an item!")
async def challenge(ctx, arg):
    await ctx.respond(f" <@{ctx.author.id} challenged " + arg + " to draw " + generate_item_name() + "!")


bot.run(TOKEN)
