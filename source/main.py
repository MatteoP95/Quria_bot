import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
import locale
import asyncio


bot = commands.Bot(command_prefix="//", intents=discord.Intents.all())

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print("BOT CONNESSO")
    print("------------------------------------")


selezione = {}
num_partecipanti = 0


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOTTONE
class Button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

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
            selezione[interaction.user.id][
                "max_players"
            ] = 6  # Imposta il valore di max_players per i Raid
            await interaction.response.send_message(view=Nome1View(), ephemeral=True)
        elif self.values[0] == "Dungeon":
            await interaction.response.send_message(view=Nome2View(), ephemeral=True)
        else:
            selezione[interaction.user.id][
                "max_players"
            ] = 3  # Imposta il valore di max_players per le altre attività
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
        if self.values[0] == "Prove di Osiride" or self.values[0] == "Competitiva":
            selezione[interaction.user.id][
                "max_players"
            ] = 3  # Imposta il valore di max_players per le Prove di Osiride
        elif self.values[0] == "Stendardo di Ferro" or self.values[0] == "Crogiolo":
            selezione[interaction.user.id][
                "max_players"
            ] = 6  # Imposta il valore di max_players per Stendardo di Ferro e Crogiolo
        elif self.values[0] == "Privata":
            selezione[interaction.user.id][
                "max_players"
            ] = 12  # Imposta il valore di max_players per Privata
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
            discord.SelectOption(label="Oggi"),
            discord.SelectOption(label="Domani"),
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
        giorni_settimana = {
            "Lunedì": 0,
            "Martedì": 1,
            "Mercoledì": 2,
            "Giovedì": 3,
            "Venerdì": 4,
            "Sabato": 5,
            "Domenica": 6,
        }
        oggi = datetime.now()
        if self.values[0] == "Oggi":
            giorno_selezionato = list(giorni_settimana.keys())[oggi.weekday()]
        elif self.values[0] == "Domani":
            giorno_selezionato = list(giorni_settimana.keys())[(oggi.weekday() + 1) % 7]
        else:
            giorno_selezionato = self.values[0]

        selezione[interaction.user.id]["Giorno"] = giorno_selezionato
        differenza_giorni = (
            giorni_settimana[giorno_selezionato] - oggi.weekday() + 7
        ) % 7
        data_evento = oggi + timedelta(days=differenza_giorni)

        # Aggiorna la data dell'evento nella selezione dell'utente
        selezione[interaction.user.id]["Data evento"] = data_evento

        # Prosegui con la selezione dell'ora
        await interaction.response.send_message(
            view=OraView(giorno_selezionato), ephemeral=True
        )


class GiornoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Giorno())


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ora


class Ora(discord.ui.Select):
    def __init__(self, giorno_selezionato):
        # Ottieni l'ora e il giorno attuali
        ora_attuale = datetime.now().hour
        giorno_attuale = datetime.now().strftime("%A")
        minuti_attuali = datetime.now().minute

        # Mappa i nomi dei giorni in inglese ai corrispondenti nomi in italiano
        giorni_italiano = {
            "Monday": "Lunedì",
            "Tuesday": "Martedì",
            "Wednesday": "Mercoledì",
            "Thursday": "Giovedì",
            "Friday": "Venerdì",
            "Saturday": "Sabato",
            "Sunday": "Domenica",
        }

        # Traduci il giorno attuale in italiano
        giorno_attuale_italiano = giorni_italiano[giorno_attuale]

        # Se l'utente ha selezionato 'Oggi', allora rendi selezionabili solo le ore future
        if giorno_selezionato == giorno_attuale_italiano:
            if minuti_attuali > 45:
                options = [
                    discord.SelectOption(label=str(i).zfill(2))
                    for i in range(ora_attuale + 1, 25)
                ]
            else:
                options = [
                    discord.SelectOption(label=str(i).zfill(2))
                    for i in range(ora_attuale, 25)
                ]
        else:
            options = [
                discord.SelectOption(label=str(i).zfill(2)) for i in range(8, 25)
            ]

        super().__init__(placeholder="Ora", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        selezione[interaction.user.id]["Ore"] = self.values[0]
        user_selection = selezione[
            interaction.user.id
        ]  # Ottieni la selezione dell'utente
        await interaction.response.send_message(
            view=MinutiView(user_selection), ephemeral=True
        )


class OraView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Ora())


class OraView(discord.ui.View):
    def __init__(self, giorno_selezionato):
        super().__init__()
        self.add_item(Ora(giorno_selezionato))


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Minuti


class Minuti(discord.ui.Select):
    def __init__(self, user_selection):
        # Ottieni i minuti attuali
        minuti_attuali = datetime.now().minute

        # Se l'utente ha selezionato l'ora corrente, mostra solo le opzioni future
        if (
            int(user_selection.get("Ore")) == datetime.now().hour
        ):  # Converti l'ora in un numero
            if minuti_attuali < 15:
                options = [
                    discord.SelectOption(label=str(i * 15).zfill(2))
                    for i in range(1, 4)
                ]
            elif minuti_attuali < 30:
                options = [
                    discord.SelectOption(label=str(i * 15).zfill(2))
                    for i in range(2, 4)
                ]
            elif minuti_attuali < 45:
                options = [discord.SelectOption(label="45")]
            else:
                options = []  # Nessuna opzione disponibile
        else:
            options = [
                discord.SelectOption(label=str(i * 15).zfill(2)) for i in range(4)
            ]

        super().__init__(
            placeholder="Minuti", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        # Ritarda la risposta all'interazione
        await interaction.response.defer()

        selezione[interaction.user.id]["Minuti"] = self.values[0]

        # Ottieni i valori di 'Giorno', 'Ore' e 'Minuti'
        Giorno = selezione[interaction.user.id]["Giorno"]
        Ore = selezione[interaction.user.id]["Ore"]
        Minuti = selezione[interaction.user.id]["Minuti"]

        # Mappa i giorni della settimana in italiano ai corrispondenti numeri (0 = Lunedì, 1 = Martedì, ..., 6 = Domenica)
        giorni_settimana = {
            "Lunedì": 0,
            "Martedì": 1,
            "Mercoledì": 2,
            "Giovedì": 3,
            "Venerdì": 4,
            "Sabato": 5,
            "Domenica": 6,
        }

        # Ottieni il giorno attuale
        oggi = datetime.now()

        # Calcola il numero di giorni fino al prossimo 'Giorno'
        differenza_giorni = (giorni_settimana[Giorno] - oggi.weekday() + 7) % 7

        # Crea la data dell'evento aggiungendo la differenza dei giorni a 'oggi'
        data_evento = oggi + timedelta(days=differenza_giorni)

        # Imposta l'ora e i minuti dell'evento
        data_evento = data_evento.replace(hour=int(Ore), minute=int(Minuti))

        # Aggiungi la data dell'evento alla selezione dell'utente
        selezione[interaction.user.id]["Data evento"] = data_evento

        await send_summary(interaction)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Embed


# Creiamo un dizionario per tenere traccia dei partecipanti per ogni evento
partecipanti_evento = {}
riserve_evento = {}


class MyButton(discord.ui.Button):
    def __init__(self, label: str, custom_id: str, style: discord.ButtonStyle):
        super().__init__(style=style, label=label, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        # Ritarda la risposta all'interazione
        await interaction.response.defer()

        # Ottieni il messaggio incorporato e il campo "Partecipanti"
        embed = interaction.message.embeds[0].to_dict()
        partecipanti = embed["fields"][-3]  # L'ultimo campo è "Partecipanti"
        riserve = embed["fields"][-1]

        # Ottieni l'ID dell'evento dal messaggio dell'interazione
        evento_id = interaction.message.id

        # Se l'evento non è ancora nel dizionario partecipanti_evento, aggiungilo
        if evento_id not in partecipanti_evento:
            partecipanti_evento[evento_id] = []
            riserve_evento[evento_id] = []

        max_players = selezione[interaction.user.id]["max_players"]

        if self.custom_id == "button1":  # Se l'utente ha cliccato il pulsante verde
            # Aggiungi l'utente alla lista dei partecipanti solo se non è già presente
            user_name = f"{interaction.user.name}"
            if user_name not in partecipanti["value"]:
                # Controllo se l'attività è un Raid e se il numero di partecipanti ha raggiunto il limite
                if len(partecipanti_evento[evento_id]) >= max_players:
                    riserve["value"] += f"\n{user_name}"
                    riserve_evento[evento_id].append(interaction.user)
                else:
                    partecipanti["value"] += f"\n{user_name}"
                    partecipanti_evento[evento_id].append(interaction.user)
            else:
                await interaction.followup.send(
                    "Il tuo nome è già nella lista dei partecipanti.", ephemeral=True
                )
                return
        elif self.custom_id == "button2":  # Se l'utente ha cliccato il pulsante rosso
            # Rimuovi l'utente dalla lista dei partecipanti
            user_name = f"{interaction.user.name}"
            if user_name in partecipanti["value"]:
                partecipanti["value"] = partecipanti["value"].replace(user_name, "")
                partecipanti_evento[evento_id].remove(interaction.user)
            else:
                await interaction.followup.send(
                    "Il tuo nome non è nella lista dei partecipanti.", ephemeral=True
                )
                return

        # Aggiorna il campo "Partecipanti" con il numero corretto di partecipanti
        partecipanti["name"] = (
            f"Partecipanti: {len(partecipanti_evento[evento_id])} / {max_players}"
        )
        if len(riserve_evento[evento_id]) != 0:
            riserve["name"] = f"Riserve : {len(riserve_evento[evento_id])}"

        # Crea un nuovo messaggio incorporato con il campo aggiornato
        new_embed = discord.Embed.from_dict(embed)

        # Modifica il messaggio per aggiornare il messaggio incorporato
        await interaction.message.edit(embed=new_embed, view=ButtonView())


class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MyButton("+", "button1", discord.ButtonStyle.green))
        self.add_item(MyButton("-", "button2", discord.ButtonStyle.red))
        self.add_item(MyButton("EDIT", "button3", discord.ButtonStyle.gray))


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
            name="Modalità", value=user_selection.get("Modalità", ""), inline=False
        )

    # Mappa i nomi dei giorni e dei mesi in inglese ai corrispondenti nomi in italiano
    giorni_italiano = [
        "Lunedì",
        "Martedì",
        "Mercoledì",
        "Giovedì",
        "Venerdì",
        "Sabato",
        "Domenica",
    ]
    mesi_italiano = [
        "Gennaio",
        "Febbraio",
        "Marzo",
        "Aprile",
        "Maggio",
        "Giugno",
        "Luglio",
        "Agosto",
        "Settembre",
        "Ottobre",
        "Novembre",
        "Dicembre",
    ]

    # Ottieni la data dell'evento
    data_evento = user_selection.get("Data evento")

    # Ottieni il giorno della settimana e il mese in italiano
    giorno_italiano = giorni_italiano[data_evento.weekday()]
    mese_italiano = mesi_italiano[data_evento.month - 1]

    # Formatta la data nel formato 'Giorno GG Mese'
    data_formattata = f"{giorno_italiano} {data_evento.day} {mese_italiano}"

    embed.add_field(
        name="Data",
        value=f"`{data_formattata} - {user_selection.get('Ore', '')}:{user_selection.get('Minuti', '')}`",
        inline=True,
    )

    embed.add_field(
        name="\u200b",  # carattere spazio invisibile
        value="\u200b",
        inline=True,
    )

    # Calcola il tempo rimanente fino all'evento (in secondi)
    tempo_rimanente = (data_evento - datetime.now()).total_seconds()

    # Calcola il tempo rimanente in giorni, ore e minuti
    giorni_rimanenti = tempo_rimanente // (24 * 3600)
    ore_rimanenti = (tempo_rimanente % (24 * 3600)) // 3600
    minuti_rimanenti = (tempo_rimanente % 3600) // 60

    # Formatta il tempo rimanente
    if giorni_rimanenti >= 1:
        tempo_rimanente_formattato = f"{int(giorni_rimanenti)} Giorni"
    elif ore_rimanenti > 1:
        tempo_rimanente_formattato = f"{int(ore_rimanenti)} Ore"
    elif ore_rimanenti == 1:
        tempo_rimanente_formattato = "60 Minuti"
    elif minuti_rimanenti >= 10:
        tempo_rimanente_formattato = f"{int(minuti_rimanenti)} Minuti"
    else:
        tempo_rimanente_formattato = "Iniziato"

    # Aggiungi il tempo rimanente come un campo nel messaggio incorporato
    embed.add_field(
        name="Inizia tra:",
        value=f"`{tempo_rimanente_formattato}`",
        inline=True,
    )

    max_players = user_selection.get("max_players", 3)

    embed.add_field(
        name=f"Partecipanti: {num_partecipanti} / {max_players}",
        value="",
        inline=True,
    )
    embed.add_field(
        name="\u200b",  # carattere spazio invisibile
        value="\u200b",
        inline=True,
    )
    embed.add_field(
        name="",
        value="",
        inline=True,
    )

    # Invia il messaggio incorporato all'utente
    message = await interaction.channel.send(embed=embed, view=ButtonView())

    # Avvia il task per inviare le notifiche
    asyncio.create_task(invia_notifiche(data_evento, message))

    # Aggiungi questa linea per avviare il task per aggiornare l'embed
    asyncio.create_task(aggiorna_embed(message, data_evento))


async def aggiorna_embed(message, data_evento):
    while True:  # Loop infinito
        # Calcola il tempo rimanente
        tempo_rimanente = (data_evento - datetime.now()).total_seconds()

        # Calcola il tempo rimanente in giorni, ore e minuti
        giorni_rimanenti = tempo_rimanente // (24 * 3600)
        ore_rimanenti = (tempo_rimanente % (24 * 3600)) // 3600
        minuti_rimanenti = (tempo_rimanente % 3600) // 60

        # Formatta il tempo rimanente
        if giorni_rimanenti == 1:
            tempo_rimanente_formattato = f"{int(giorni_rimanenti)} Giorno"
        elif giorni_rimanenti > 1:
            tempo_rimanente_formattato = f"{int(giorni_rimanenti)} Giorni"
        elif ore_rimanenti == 1:
            tempo_rimanente_formattato = f"{int(ore_rimanenti)} Ora"
        elif ore_rimanenti > 1:
            tempo_rimanente_formattato = f"{int(ore_rimanenti)} Ore"
        elif minuti_rimanenti == 1:
            tempo_rimanente_formattato = f"{int(minuti_rimanenti)} Minuto"
        elif minuti_rimanenti > 0:
            tempo_rimanente_formattato = f"{int(minuti_rimanenti+1)} Minuti"
        elif minuti_rimanenti == 0:
            tempo_rimanente_formattato = "Iniziato"

        # Ottieni l'embed dal messaggio
        embed = message.embeds[0]

        # Trova l'indice del campo "Inizia tra:"
        for i, field in enumerate(embed.fields):
            if field.name == "Inizia tra:":
                break
        else:
            print("Campo 'Inizia tra:' non trovato")
            return

        # Aggiorna il campo "Inizia tra:"
        embed.set_field_at(
            i, name="Inizia tra:", value=f"`{tempo_rimanente_formattato}`", inline=True
        )

        # Modifica il messaggio per aggiornare l'embed
        await message.edit(embed=embed)

        # Aspetta un po' prima del prossimo aggiornamento
        if giorni_rimanenti >= 1:
            await asyncio.sleep(3600)  # Aggiorna ogni ora
        elif ore_rimanenti >= 1:
            await asyncio.sleep(600)  # Aggiorna ogni 10 minuti
        else:
            await asyncio.sleep(60)  # Aggiorna ogni minuto


async def invia_notifiche(data_evento, message):
    # Calcola il tempo rimanente fino all'evento (in secondi)
    tempo_rimanente = (
        data_evento - datetime.now()
    ).total_seconds() - 3600  # sottrai un'ora

    if tempo_rimanente > 0:
        # Attendi fino a quando non manca un'ora all'evento
        await asyncio.sleep(tempo_rimanente)

        # Ottieni l'URL del messaggio dell'evento
        url_messaggio = message.jump_url

        # Invia un messaggio privato a tutti i partecipanti
        for user in partecipanti_evento[data_evento]:
            if user.dm_channel is None:
                await user.create_dm()
            await user.dm_channel.send(f"Ehi! Manca un'ora all'Evento")


# Puoi chiamare questa funzione ogni volta che crei un nuovo evento
async def crea_evento(data_evento):
    asyncio.create_task(invia_notifiche(data_evento))


class MinutiView(discord.ui.View):
    def __init__(self, user_selection):
        super().__init__()
        self.add_item(Minuti(user_selection))


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
