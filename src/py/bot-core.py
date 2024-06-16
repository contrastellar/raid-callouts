"""
This module is the listener to discord.
This module will listen to the discord server for two things:
1. the !schedule command -- which will report the current callouts
2. the !callout command -- which will allow users to add a new scheduled callout
3. the !pulls command -- which will report the total pulls for the current raid
4. Optional -- the !add_report command -- which will allow users to add a new report, to be parsed by the database
5. optional -- the !remove_report command -- which will do the opposite of !add_report, it will require the URL of the report to be removed
6. 

@author: Gabriella 'contrastellar' Agathon
"""
import discord
import psycopg2
import helper
import helper.request_helper, helper.db_helper


DATABASE_CONN = None
# Guild is Errai, my private server
# Channel is #dev, in Errai
SAMPLE_GUILD_ID = 477298331777761280 # TODO needs to be dynamically loaded in the future
SAMPLE_CHANNEL_ID = 927271992216920146 # TODO needs to be dynamically loaded in the future

# Database related constants
DB_URL = '' # TODO needs to be loaded from a file
DB_USER = '' # TODO needs to be loaded from a file
DB_PASS = '' # TODO needs to be loaded from a file

# To be used for the optional commands -- !add_report and !remove_report
FFLOGS_URL = 'https://www.fflogs.com/api/v2/client' # TODO needs to be loaded from a file
FFLOGS_TOKEN = '' # TODO needs to be loaded from a file
FFLOGS_USER = '' # TODO needs to be loaded from a file


intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.presences = False

client = discord.Client(intents=intents)

@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')
    return


@client.event
async def on_message(message: discord.message) -> None:
    message_content: discord.message = message.content # Shorthand to grab the message.content
    channel_id: int = message.channel.id # Shorthand to grab the message.channel.id
    guild_id: int = message.guild.id     # Shorthand to grab the messsage.guild.id
    # These should remove the need to hardcode the channel and guild we're talking to

    if(message_content.startswith('!pulls')):
        # TODO
        # This is the command that will report the total pulls for the current raid
        return



REQUESTS_HELPER = REQUESTS_HELPER = helper.request_helper.RequestsHelper(FFLOGS_URL, FFLOGS_TOKEN, FFLOGS_USER)
DATABASE_CONN = helper.db_helper.DBHelper(DB_URL, DB_USER, DB_PASS)

TOKEN = open('discord.token', encoding='utf-8').read()
client.run(TOKEN)
