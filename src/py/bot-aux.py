"""
This module is the automated poster to discord.
This module will post to the discord whenever the script is run, detailing the callouts for the current raid for the next seven days.
This automation will be run on a daily basis, through a cron job + docker.

@author: Gabriella 'contrastellar' Agathon
"""
import argparse
import os
import discord
import helper.db_helper


DATABASE_CONN = None

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.presences = False

client = discord.Client(intents=intents)

NUMBER_OF_DAYS = 7

parser: argparse.ArgumentParser = argparse.ArgumentParser(prog='callouts aux', 
                        description='The poster for the callouts bot functionality')

parser.add_argument('database')
parser.add_argument('token')
parser.add_argument('guild_id', type=int)
parser.add_argument('channel_id', type=int)

args = parser.parse_args()

@client.event
async def on_ready():
    # Exit without pushing anything to the channel/guild
    if 'RAID_CALLOUTS_DEV' in os.environ:
        callouts = DATABASE_CONN.query_callouts(NUMBER_OF_DAYS)
        formatted_callouts = DATABASE_CONN.format_list_of_callouts(callouts)
        output = f'Callouts for the next {NUMBER_OF_DAYS} days:\n' + formatted_callouts
        print(output)
        await client.close()
        return
    
    print(f'{client.user} has connected.')
    print(args.guild_id)
    GUILD: discord.Guild = client.get_guild(args.guild_id)
    CHANNEL: discord.abc.GuildChannel = GUILD.get_channel(args.channel_id)
    callouts = DATABASE_CONN.query_callouts(NUMBER_OF_DAYS)
    formatted_callouts = DATABASE_CONN.formatted_list_of_callouts(callouts)
    output = f'Callouts for the next {NUMBER_OF_DAYS} days:\n' + formatted_callouts
    await CHANNEL.send(output)
    await client.close() # Another way to exit, a little bit cleaner than exit(0)
    return

DATABASE_CONN = helper.db_helper.DBHelper(args.database)
TOKEN = open(args.token, encoding='utf-8').read()
client.run(TOKEN)
