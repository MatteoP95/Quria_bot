import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    print("----------------------------------------")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, i am Quria!")


client.run(TOKEN)
