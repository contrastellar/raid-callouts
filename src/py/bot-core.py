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

def cleanup_invalidate() -> None:
    DATABASE_CONN.isProcedureQueued = False
    return

def delete_invalidate() -> None:
    DATABASE_CONN.isUnregisterQueued = False

@client.event
async def on_ready() -> None:
    await client.tree.sync()
    print(f'{client.user} has connected to Discord!')
    return

@client.tree.command()
async def help(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()
    output = "Are you having issues with the bot? Please contact contrastellar with any questions!"
    interaction.response.send_message(output)
    return

@client.tree.command()
async def registercharacter(interaction: discord.Interaction, character_name: str) -> None:
    delete_invalidate()
    cleanup_invalidate()
    user_id = interaction.user.id
    user_nick = interaction.user.display_name

    try:
        DATABASE_CONN.register_char_name(user_id, character_name)
    except psycopg2.errors.UniqueViolation:
        await interaction.response.send_message(f'User {user_nick} -- you have already registered a character! Please contact contrastellar with questions!')
    else:
        await interaction.response.send_message(f'User {user_nick} -- you have registered your discord account with {character_name}! Please contact contrastellar with questions!')
    return


@client.tree.command()
async def checkcharname(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()
    charname: str = DATABASE_CONN.return_char_name(interaction.user.id)
    
    if charname == "":
        await interaction.response.send_message("You have not registered! Please do with /registercharacter")
        return
    if interaction.user.id == 151162055142014976:
        await interaction.response.send_message("You are: " + charname + "... in case you forgot.")
        return
    
    await interaction.response.send_message("You are: " + charname)
    return


@client.tree.command()
async def removeregistration(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()
    await interaction.response.send_message("To remove your registration with the boss, please run the `/confirm_unregister` command\nPlease be aware that this will also remove all of your callouts from the bot! ***This is in an irreversable action!***")
    DATABASE_CONN.isUnregisterQueued = True
    return


@client.tree.command()
async def confirm_unregister(interaction: discord.Interaction) -> None:
    cleanup_invalidate()

    userID = interaction.user.id
    userNick = interaction.user.nick

    await interaction.response.defer(thinking=True)
    print(f"Removing {userID} from the database!")

    DATABASE_CONN.remove_registration(userID, DATABASE_CONN.isUnregisterQueued)

    await interaction.followup.send(f"{userNick}, you have been unregistered!")
    delete_invalidate()


@client.tree.command()
async def invalidate_unregister(interaction: discord.Interaction) -> None:
    cleanup_invalidate()
    delete_invalidate()
    print(f"User deletion has been invalidated! Aborting process!")

    await interaction.response.send_message("Unregister has been invalidated!")

    return


@client.tree.command()
async def ping(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()
    user_id = interaction.user.id
    await interaction.response.send_message(f'Pong! {user_id}')
    return


@client.tree.command()
async def cleanup(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()
    numberToBeAffected: int = DATABASE_CONN.number_affected_in_cleanup()
    await interaction.response.send_message(f"Is the bot being weird or slow? You can try the `/validate_cleanup` command to clear out old database entries!\nBe warned that this is an admin-level command, and may have unintended side effects!\n{numberToBeAffected} rows will be affected by the `/validate_cleanup` command!")
    DATABASE_CONN.isProcedureQueued = True
    print(f"Bot has been primed for cleanup!")
    return


@client.tree.command()
async def validate_cleanup(interaction: discord.Interaction) -> None:
    delete_invalidate()
    user_id = interaction.user.id
    user_nickname = interaction.user.nick
    await interaction.response.defer(thinking=True)
    print(f"{user_nickname} has called validate_cleanup!\n\nCalling now.")

    number_rows_affected: int

    try: 
        number_rows_affected = DATABASE_CONN.call_cleanup(DATABASE_CONN.isProcedureQueued)
    except Exception as e:
        print(e)
        await interaction.followup.send("Something happened! This message is to inform <@181187505448681472> of this error!")
        return
    
    print(f"cleanup should be complete. Setting queue variable to False")
    DATABASE_CONN.isProcedureQueued = False
    await interaction.followup.send(f"Database has been cleaned!\n\n{number_rows_affected} rows have been purged!")
    
    return

async def invalidate_cleanup(interaction: discord.Interaction) -> None:
    delete_invalidate()
    invalidate_cleanup()

    await interaction.response.defer(thinking=True)

    print(f"{interaction.user.id} has called the invalidate command!")
    print(f"Cleanup has been invalidated!")
    await interaction.followup.send("The queued action has been cancelled!")

    return


@client.tree.command()
async def callout(interaction: discord.Interaction, date_of_callout: str, reason: str ='') -> None:
    delete_invalidate()
    cleanup_invalidate()
    user_id = interaction.user.id
    user_nick = interaction.user.display_name

    user_char_name = DATABASE_CONN.return_char_name(user_id)

    try:
        DATABASE_CONN.add_callout(user_id=user_id, callout=date_of_callout, reason=reason, nickname=user_nick, char_name=user_char_name)
    except psycopg2.errors.UniqueViolation:
        await interaction.response.send_message(f'User {user_char_name} -- you have already added a callout for {date_of_callout} with reason: {reason}')
    except psycopg2.errors.InvalidDatetimeFormat:
        await interaction.response.send_message(f'User {user_char_name} -- please format the date as one of the following: \n YYYY-MM-DD \n MM-DD-YYYY \n YYYYMMDD')
    except psycopg2.errors.ForeignKeyViolation:
        await interaction.response.send_message(f'User {user_nick} -- please register with the bot using the following command!\n /registercharacter\n Please use your in-game name!')
    else:
        await interaction.response.send_message(f'User {user_char_name} -- you added a callout for {date_of_callout} with reason: {reason}')


@client.tree.command()
async def remove_callout(interaction: discord.Interaction, date_of_callout: str) -> None:
    delete_invalidate()
    cleanup_invalidate()
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
    delete_invalidate()
    cleanup_invalidate()
    callouts: list = DATABASE_CONN.query_callouts(days=days)
    callouts: str = DATABASE_CONN.formatted_list_of_callouts(callouts)
    await interaction.response.send_message(f'Callouts for the next {days} days:\n{callouts}')
    return


args: argparse.Namespace = parser.parse_args()

# To be used for reading/writing to the database 
# #will not handle the parsing of the returns from the db
DATABASE_CONN = helper.db_helper.DBHelper(args.database)

TOKEN = open(args.token, encoding='utf-8').read()
client.run(TOKEN)
