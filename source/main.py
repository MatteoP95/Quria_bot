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


# LISTE DEL MODAL
attivita = ["PVE", "PVP"]
PVP = ["Prove di Osiride", "Stendardo di Ferro", "Crogiolo", "Privata"]
PVE = [
    "Raid",
    "Dungeon",
    "Cala la Notte",
    "Quest Esotica",
    "Attività Stagionale",
]
Raid = [
    "Volta di Vetro",
    "La Fine di Crota",
    "La Caduta di un Re",
    "Ultimo Desiderio",
    "Giardino della Salvezza",
    "Cripta di Pietrafonda",
    "Promessa del Discepolo",
    "Radice degli Incubi",
]
Dungeon = [
    "Trono Infranto",
    "Fossa dell'Eresia",
    "Profezia",
    "Morsa della Cupidigia",
    "Dualità",
    "Pinnacolo dell'Osservatrice",
    "Spettri del Profondo",
    "Rovina della Signora della Guerra",
]

client.run(TOKEN)
