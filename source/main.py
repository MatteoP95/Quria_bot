import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


bot = commands.Bot(command_prefix="//", intents=discord.Intents.all())

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print("BOT CONNESSO")
    print("------------------------------------")


selezione = {}


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOTTONE
class Button(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Attività", style=discord.ButtonStyle.red)
    async def inviteBtn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await event(interaction)


@bot.command()
async def button(ctx: commands.Context):
    await ctx.send(view=Button())


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# TIPO


class Tipo(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="PVE"),
            discord.SelectOption(label="PVP"),
        ]
        super().__init__(
            placeholder="PVE/PVP", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id] = {"Tipo": self.values[0]}
        if self.values[0] == "PVE":
            await interaction.response.send_message(view=PVEView(), ephemeral=True)
        elif self.values[0] == "PVP":
            await interaction.response.send_message(view=PVPView(), ephemeral=True)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# PVE


class PVE(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Raid"),
            discord.SelectOption(label="Dungeon"),
            discord.SelectOption(label="Cala la Notte"),
            discord.SelectOption(label="Quest Esotica"),
            discord.SelectOption(label="Quest Stagionale"),
        ]
        super().__init__(
            placeholder="Attività", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id]["Attività"] = self.values[0]
        if self.values[0] == "Raid":
            await interaction.response.send_message(view=Nome1View(), ephemeral=True)
        elif self.values[0] == "Dungeon":
            await interaction.response.send_message(view=Nome2View(), ephemeral=True)
        else:
            await interaction.response.send_message(view=GiornoView(), ephemeral=True)


class Nome1(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Volta di Vetro"),
            discord.SelectOption(label="La Fine di Crota"),
            discord.SelectOption(label="La Caduta di un Re"),
            discord.SelectOption(label="Ultimo Desiderio"),
            discord.SelectOption(label="Giardino della Salvezza"),
            discord.SelectOption(label="Cripta di Pietrafonda"),
            discord.SelectOption(label="Promessa del Discepolo"),
            discord.SelectOption(label="Radice degli Incubi"),
        ]
        super().__init__(
            placeholder="Raid", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id]["Raid"] = self.values[0]
        await interaction.response.send_message(view=GiornoView(), ephemeral=True)


class Nome1View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Nome1())


class Nome2(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Trono Infranto"),
            discord.SelectOption(label="Fossa dell'Eresia"),
            discord.SelectOption(label="Profezia"),
            discord.SelectOption(label="Morsa della Cupidigia"),
            discord.SelectOption(label="Dualità"),
            discord.SelectOption(label="Pinnacolo dell'Osservatrice"),
            discord.SelectOption(label="Spettri del Profondo"),
            discord.SelectOption(label="Rovina della Signora della Guerra"),
        ]
        super().__init__(
            placeholder="Dungeon", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id]["Dungeon"] = self.values[0]
        await interaction.response.send_message(view=GiornoView(), ephemeral=True)


class Nome2View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Nome2())


class PVEView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PVE())


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# PVP


class PVP(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Prove di Osiride"),
            discord.SelectOption(label="Stendardo di Ferro"),
            discord.SelectOption(label="Competitiva"),
            discord.SelectOption(label="Privata"),
            discord.SelectOption(label="Crogiolo"),
        ]
        super().__init__(
            placeholder="Modalità", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id]["Modalità"] = self.values[0]
        await interaction.response.send_message(view=GiornoView(), ephemeral=True)


class PVPView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PVP())


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Giorno


class Giorno(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Lunedì"),
            discord.SelectOption(label="Martedì"),
            discord.SelectOption(label="Mercoledì"),
            discord.SelectOption(label="Giovedì"),
            discord.SelectOption(label="Venerdì"),
            discord.SelectOption(label="Sabato"),
            discord.SelectOption(label="Domenica"),
        ]
        super().__init__(
            placeholder="Giorno", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id]["Giorno"] = self.values[0]
        await interaction.response.send_message(view=OraView(), ephemeral=True)


class GiornoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Giorno())


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ora


class Ora(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=str(i).zfill(2)) for i in range(1, 25)]
        super().__init__(placeholder="Ora", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id]["Ore"] = self.values[0]
        await interaction.response.send_message(view=MinutiView(), ephemeral=True)


class OraView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Ora())


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Minuti


class Minuti(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=str(i * 15).zfill(2)) for i in range(4)]
        super().__init__(
            placeholder="Minuti", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id]["Minuti"] = self.values[0]
        await send_summary(interaction)


async def send_summary(interaction: discord.Interaction):
    # Ottieni l'oggetto Selezione per l'utente corrente
    user_selection = selezione[interaction.user.id]

    # Crea un messaggio incorporato con le informazioni selezionate
    embed = discord.Embed(
        title=f"EVENTO - {user_selection.get('Tipo', '')}", color=0xFF0000
    )

    # Aggiungi ogni selezione come un campo nel messaggio incorporato
    if user_selection.get("Tipo") == "PVE":

        if user_selection.get("Attività") == "Raid":
            embed.add_field(
                name="Raid", value=user_selection.get("Raid", ""), inline=False
            )
        if user_selection.get("Attività") == "Dungeon":
            embed.add_field(
                name="Dungeon", value=user_selection.get("Dungeon", ""), inline=False
            )
        elif (
            user_selection.get("Attività") != "Dungeon"
            and user_selection.get("Attività") != "Raid"
        ):
            embed.add_field(
                name="Attività", value=user_selection.get("Attività", ""), inline=False
            )

    if user_selection.get("Tipo") == "PVP":
        embed.add_field(
            name="Modalità", value=user_selection.get("Modalità", ""), inline=True
        )

    embed.add_field(
        name="Giorno",
        value=user_selection.get("Giorno", ""),
        inline=True,
    )
    embed.add_field(
        name="Ora",
        value=f"{user_selection.get('Ore', '')} : {user_selection.get('Minuti', '')}",
        inline=True,
    )

    # Invia il messaggio incorporato all'utente
    await interaction.response.send_message(embed=embed)


class MinutiView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Minuti())


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class TypeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Tipo())


async def create_event(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Crea un Evento!", view=TypeView(), ephemeral=True
    )


@bot.command()
async def event(ctx: commands.context):
    await create_event(ctx)


bot.run(TOKEN)
