"""
This module is the automated poster to discord.
This module will post to the discord whenever the script is run, detailing the callouts for the current raid for the next seven days.
This automation will be run on a daily basis, through a cron job + docker.

@author: Gabriella 'contrastellar' Agathon
"""
import os
import discord
import helper.db_helper


DATABASE_CONN = None
# Guild is Errai, my private server
# Channel is #dev, in Errai
ERRAI_GUILD_ID = 477298331777761280 # FIXME needs to be dynamically loaded in the future
ERRAI_CHANNEL_ID = 927271992216920146 # FIXME needs to be dynamically loaded in the future

# Guild for schedule callouts for FA
FA_GUILD_ID = 865781604881530940
FA_CHANNEL_ID = 888844785274724362

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.presences = False

DATABASE_CONN = helper.db_helper.DBHelper()
client = discord.Client(intents=intents)

NUMBER_OF_DAYS = 7

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

    GUILD = client.get_guild(FA_GUILD_ID)
    CHANNEL = GUILD.get_channel(FA_CHANNEL_ID)
    callouts = DATABASE_CONN.query_callouts(NUMBER_OF_DAYS)
    formatted_callouts = DATABASE_CONN.format_list_of_callouts(callouts)
    output = f'Callouts for the next {NUMBER_OF_DAYS} days:\n' + formatted_callouts
    await CHANNEL.send(output)
    await client.close() # Another way to exit, a little bit cleaner than exit(0)

TOKEN = open('discord.token', encoding='utf-8').read()
client.run(TOKEN)
