import os

import discord


TOKEN = "MTE3NjQ1NzAyODgxMDU5MjMwNg.GmUJw2.o516OQ3tDtwEUzA0y_UUDz93sFBImzmi2MaRv0"

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


client.run(TOKEN)
