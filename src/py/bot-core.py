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
import datetime
import discord
import psycopg2
from discord.ext import commands
import helper.request_helper, helper.db_helper

DAYS_FOR_CALLOUTS = 7

DATABASE_CONN = None
# Guild is Errai, my private server
# Channel is #dev, in Errai
ERRAI_GUILD_ID = int(477298331777761280) # FIXME needs to be dynamically loaded in the future
ERRAI_CHANNEL_ID = int(927271992216920146) # FIXME needs to be dynamically loaded in the future

FA_GUILD_ID = int(865781604881530940)
FA_CALLOUT_CHANNEL_ID = int(888844785274724362)

# To be used for the optional commands -- !add_report and !remove_report
FFLOGS_URL = 'https://www.fflogs.com/api/v2/client' # FIXME needs to be loaded from a file
FFLOGS_TOKEN = '' # FIXME needs to be loaded from a file
FFLOGS_USER = '' # FIXME needs to be loaded from a file


intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.presences = False

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready() -> None:
    for guild in client.guilds:
        print(f'{guild.name} (id: {guild.id})')

    await client.tree.sync()
    print(f'{client.user} has connected to Discord!')
    return


@client.tree.command()
async def ping(interaction: discord.Interaction) -> None:
    user_id = interaction.user.id
    await interaction.response.send_message(f'Pong! {user_id}')


@client.tree.command()
async def callout(interaction: discord.Interaction, date_of_callout: str, reason: str ='') -> None:
    user_id = interaction.user.id
    user_nick = interaction.user.display_name
    try:
        DATABASE_CONN.add_callout(user_id=user_id, callout=date_of_callout, reason=reason, nickname=user_nick)
    except psycopg2.errors.UniqueViolation:
        await interaction.response.send_message(f'User {user_id}/{user_nick} -- you have already added a callout for {date_of_callout} with reason: {reason}')
    else:
        print(f'User {user_id}/{user_nick} added a callout for {date_of_callout} with reason: {reason}')
        await interaction.response.send_message(f'User {user_id}/{user_nick} added a callout for {date_of_callout} with reason: {reason}')


@client.tree.command()
async def schedule(interaction: discord.Interaction, days: int = DAYS_FOR_CALLOUTS) -> None:
    user_id = interaction.user.id
    await interaction.response.send_message(f'Callouts for the next {days} days: {DATABASE_CONN.query_callouts(days=days)}')


@client.event
async def on_message(message: discord.message.Message) -> None:
    message_content: discord.message.Message.content = message.content # Shorthand to grab the message.content
    channel_id: int = message.channel.id # Shorthand to!! grab the message.channel.id
    guild_id: int = message.guild.id     # Shorthand to grab the messsage.guild.id
    # These should remove the need to hardcode the channel and guild we're talking to


    if(message_content.startswith('!schedule')):
        if guild_id != ERRAI_GUILD_ID and guild_id != FA_GUILD_ID:
            await message.reply(f'This command is not available in this server.')
            return

        if channel_id != ERRAI_CHANNEL_ID and channel_id != FA_CALLOUT_CHANNEL_ID:        
            await message.reply(f'This command is not available in this channel.')
            return
        
        response = DATABASE_CONN.query_callouts(days=DAYS_FOR_CALLOUTS)
        await message.reply(f'Callouts for the next {DAYS_FOR_CALLOUTS} days: {response}')

    # The !callout command -- which will allow users to add a new scheduled callout
    # This is gonna be wonky because we're going to need to parse the message.content
    if(message_content.startswith('!callout')):
        if guild_id != ERRAI_GUILD_ID and guild_id != FA_GUILD_ID:
            await message.reply(f'This command is not available in this server.')
            return
        
        if channel_id != ERRAI_CHANNEL_ID and channel_id != FA_CALLOUT_CHANNEL_ID:        
            await message.reply(f'This command is not available in this channel.')
            return

        #TODO parse message_content for the user's ID, and nickname
        user_id = message.author.id
        nickname = message.author.nick

        # TODO parse message_content for the date


        # This is the command that will allow users to add a new scheduled callout
        await message.reply(f'Callout added for {message.author.id}')
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
