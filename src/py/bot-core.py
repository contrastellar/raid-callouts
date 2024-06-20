"""
This module is the listener to discord.
This module will listen to the discord server for two things:
1. the !schedule command -- which will report the current callouts for the next 7 days
2. the !callout command -- which will allow users to add a new scheduled callout
3. Optional -- the !pulls command -- which will report the total pulls for the current raid
4. Optional -- the !add_report command -- which will allow users to add a new report, to be parsed by the database
5. optional -- the !remove_report command -- which will do the opposite of !add_report, it will require the URL of the report to be removed
6. 

@author: Gabriella 'contrastellar' Agathon
"""
import discord
import helper.request_helper, helper.db_helper

DAYS_FOR_CALLOUTS = 7

DATABASE_CONN = None
# Guild is Errai, my private server
# Channel is #dev, in Errai
SAMPLE_GUILD_ID = 477298331777761280 # TODO needs to be dynamically loaded in the future
SAMPLE_CHANNEL_ID = 927271992216920146 # TODO needs to be dynamically loaded in the future

FA_GUILD_ID = 865781604881530940
FA_CALLOUT_CHANNEL_ID = 888844785274724362

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
async def on_message(message: discord.message.Message) -> None:
    message_content: discord.message.Message = message.content # Shorthand to grab the message.content
    channel_id: int = message.channel.id # Shorthand to grab the message.channel.id
    guild_id: int = message.guild.id     # Shorthand to grab the messsage.guild.id
    # These should remove the need to hardcode the channel and guild we're talking to

    if(message_content.startswith('!schedule')):
        if guild_id is not SAMPLE_GUILD_ID or guild_id is not FA_GUILD_ID:
            await message.reply(f'This command is not available in this server.')
            return

        if channel_id is not SAMPLE_CHANNEL_ID or channel_id is not FA_CALLOUT_CHANNEL_ID:        
            await message.reply(f'This command is not available in this channel.')
            return


    if(message_content.startswith('!pulls')):
        # TODO OPTIONAL -- the !pulls command
        # This is the command that will report the total pulls for the current raid
        await message.reply(f'This command is not available at this time.')
        return


# To be used for reading/writing to the database 
# #will not handle the parsing of the returns from the db
DATABASE_CONN = helper.db_helper.DBHelper()

# To be used for the optional commands -- !add_report and !remove_report, and will write to the database for the !pulls command
REQUESTS_HELPER = REQUESTS_HELPER = helper.request_helper.RequestsHelper(FFLOGS_URL, FFLOGS_TOKEN, FFLOGS_USER)

TOKEN = open('discord.token', encoding='utf-8').read()
client.run(TOKEN)
