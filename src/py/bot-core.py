"""
This module is the listener to discord.
"""
import discord
import psycopg2


DATABASE_CONN = None
# Guild is Errai, my private server
# Channel is #dev, in Errai
SAMPLE_GUILD_ID = 477298331777761280 # FIXME needs to be dynamically loaded in the future
SAMPLE_CHANNEL_ID = 927271992216920146 # FIXME needs to be dynamically loaded in the future

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.presences = False

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    return


@client.event
async def on_message(message):
    channel_id = message.channel.id
    guild_id = message.guild.id


TOKEN = open('discord.token', encoding='utf-8').read()
client.run(TOKEN)
