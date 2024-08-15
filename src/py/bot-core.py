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
import argparse
import discord
import psycopg2
from discord.ext import commands
import helper.request_helper, helper.db_helper

DAYS_FOR_CALLOUTS = 7

DATABASE_CONN = None

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.presences = False

client = commands.Bot(command_prefix='!', intents=intents)
parser: argparse.ArgumentParser = argparse.ArgumentParser(prog='callouts core', 
                        description='The listener for the callouts bot functionality')

parser.add_argument('database')
parser.add_argument('token')

@client.event
async def on_ready() -> None:
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
        await interaction.response.send_message(f'User {user_nick} -- you have already added a callout for {date_of_callout} with reason: {reason}')
    except psycopg2.errors.InvalidDatetimeFormat:
        await interaction.response.send_message(f'User {user_nick} -- please format the date as one of the following: \n YYYY-MM-DD \n MM-DD-YYYY \n YYYYMMDD')
    else:
        await interaction.response.send_message(f'User {user_nick} -- you  added a callout for {date_of_callout} with reason: {reason}')


@client.tree.command()
async def remove_callout(interaction: discord.Interaction, date_of_callout: str) -> None:
    user_id = interaction.user.id
    user_nick = interaction.user.display_name
    try:
        DATABASE_CONN.remove_callout(user_id=user_id, callout=date_of_callout)
    except psycopg2.errors.Error as e:
        await interaction.response.send_message(f'User {user_nick} -- you have not added a callout for {date_of_callout}')
    else:
        await interaction.response.send_message(f'User {user_nick} removed a callout for {date_of_callout}')


@client.tree.command()
async def schedule(interaction: discord.Interaction, days: int = DAYS_FOR_CALLOUTS) -> None:
    callouts: list = DATABASE_CONN.query_callouts(days=days)
    callouts: str = DATABASE_CONN.format_list_of_callouts(callouts)
    await interaction.response.send_message(f'Callouts for the next {days} days:\n{callouts}')
    return


args: argparse.Namespace = parser.parse_args()

# To be used for reading/writing to the database 
# #will not handle the parsing of the returns from the db
DATABASE_CONN = helper.db_helper.DBHelper(args.database)

TOKEN = open(args.token, encoding='utf-8').read()
client.run(TOKEN)
