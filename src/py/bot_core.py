# pylint: disable=consider-using-with, no-member
"""
This module is the listener to discord.
This module will listen to the discord server for two things:
1. the /schedule command -- which will report the current callouts for the next X days, where X is either supplied or is the default of 7
2. the /callout command -- which will allow users to add a new scheduled callout
3. a /ping command, to test the bot's current status!
4. a /registercharacter command, to allow users to register their character's name independently of their server nickname
5. a /checkcharname command, to allow users to verify their character's name
6. a /remove_callout command, to allow users to remove callouts that are no longer necessary
7. a /help command, to direct users to the github for this bot!

@author: Gabriella 'contrastellar' Agathon
"""

import argparse
import discord
import psycopg2
from discord.ext import commands
import helper.db_helper

# module constants
DAYS_FOR_CALLOUTS = 7
CONTRASTELLAR = 181187505448681472

DATABASE_CONN: helper.db_helper.DBHelper = None

# psycopg2 'imports'
UNIQUEVIOLATION: psycopg2.Error = psycopg2.errors.UniqueViolation
INVALIDDATETIMEFORMAT: psycopg2.Error = psycopg2.errors.InvalidDatetimeFormat
FOREIGNKEYVIOLATION: psycopg2.Error = psycopg2.errors.ForeignKeyViolation

# discord variables
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.presences = False

# client declaration
client = commands.Bot(command_prefix='!', intents=intents)

# parser declaration
parser: argparse.ArgumentParser = argparse.ArgumentParser(prog='callouts core',
                        description='The listener for the callouts bot functionality')
parser.add_argument('database')
parser.add_argument('token')


# utility methods
def cleanup_invalidate() -> None:
    DATABASE_CONN.is_procedure_queued = False


def delete_invalidate() -> None:
    DATABASE_CONN.is_unregister_queued = False


# discord commands
@client.event
async def on_ready() -> None:
    await client.tree.sync()
    print(f'{client.user} has connected to Discord!')
    return


@client.tree.command(name="help")
async def bot_help(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()
    output = "[Please visit this page for a complete manual on how to use the bot!](https://github.com/contrastellar/raid-callouts/wiki/Help!-(the-manual))"
    await interaction.response.send_message(output)
    return

@client.tree.command()
async def registercharacter(interaction: discord.Interaction, character_name: str) -> None:
    delete_invalidate()
    cleanup_invalidate()
    user_id = interaction.user.id
    user_nick = interaction.user.display_name

    try:
        DATABASE_CONN.register_char_name(user_id, character_name)
    except psycopg2.Error as e:
        char_name = DATABASE_CONN.return_char_name(user_id)
        await interaction.response.send_message(f'User {char_name} -- you have already registered a character!\n{e}')
    else:
        await interaction.response.send_message(f'{user_nick} -- you have registered your discord account with {character_name}!')
    return


@client.tree.command()
async def check_char_name(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()
    charname: str = DATABASE_CONN.return_char_name(interaction.user.id)

    if charname == "":
        await interaction.response.send_message("You have not registered! Please do with `/registercharacter`")
        return
    if interaction.user.id == 151162055142014976:
        await interaction.response.send_message("You are: " + charname + "... in case you forgot.")
        return

    await interaction.response.send_message("You are: " + charname)
    return


@client.tree.command()
async def remove_registration(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()
    await interaction.response.send_message("To remove your registration with the boss, please run the `/confirm_unregister` command\nPlease be aware that this will also remove all of your callouts from the bot! ***This is in an irreversable action!***")
    DATABASE_CONN.is_unregister_queued = True
    return


@client.tree.command()
async def validate_unregister(interaction: discord.Interaction) -> None:
    cleanup_invalidate()

    user_id = interaction.user.id
    user_nick = interaction.user.nick

    await interaction.response.defer(thinking=True)
    print(f"Removing {user_id} from the database!")

    DATABASE_CONN.remove_registration(user_id, DATABASE_CONN.is_unregister_queued)

    await interaction.followup.send(f"{user_nick}, you have been unregistered!")
    delete_invalidate()


@client.tree.command()
async def invalidate_unregister(interaction: discord.Interaction) -> None:
    cleanup_invalidate()
    delete_invalidate()
    print("User deletion has been invalidated! Aborting process!")

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
    number_to_be_affected: int = DATABASE_CONN.number_affected_in_cleanup()
    await interaction.response.send_message(f"Is the bot being weird or slow? You can try the `/validate_cleanup` command to clear out old database entries!\nBe warned that this is an admin-level command, and may have unintended side effects!\n{number_to_be_affected} rows will be affected by the `/validate_cleanup` command!\nThese entries are all in the past.")
    DATABASE_CONN.is_procedure_queued = True
    print("Bot has been primed for cleanup!")
    return


@client.tree.command()
async def validate_cleanup(interaction: discord.Interaction) -> None:
    delete_invalidate()
    user_nickname = interaction.user.nick
    await interaction.response.defer(thinking=True)
    print(f"{user_nickname} has called validate_cleanup!\n\nCalling now.")

    number_rows_affected: int

    try:
        number_rows_affected = DATABASE_CONN.call_cleanup(DATABASE_CONN.is_procedure_queued)
    except psycopg2.Error as e:
        print(e)
        await interaction.followup.send(f"Something happened! This message is to inform <@{CONTRASTELLAR}> of this error!\n`{e}`")
        return

    print("cleanup should be complete. Setting queue variable to False")
    DATABASE_CONN.is_procedure_queued = False
    await interaction.followup.send(f"Database has been cleaned!\n\n{number_rows_affected} rows have been purged!")

    return

@client.tree.command()
async def invalidate_cleanup(interaction: discord.Interaction) -> None:
    delete_invalidate()
    cleanup_invalidate()

    await interaction.response.defer(thinking=True)

    print(f"{interaction.user.id} has called the invalidate command!")
    print("Cleanup has been invalidated!")
    await interaction.followup.send("The queued action has been cancelled!")

    return


@client.tree.command()
async def callout(interaction: discord.Interaction, date_of_callout: str, reason: str = '', fill: str = '') -> None:
    delete_invalidate()
    cleanup_invalidate()
    user_id = interaction.user.id
    user_nick = interaction.user.display_name

    user_char_name = DATABASE_CONN.return_char_name(user_id)

    try:
        DATABASE_CONN.add_callout(user_id=user_id, callout=date_of_callout, reason=reason, nickname=user_nick, char_name=user_char_name, potential_fill=fill)
    except UNIQUEVIOLATION:
        await interaction.response.send_message(f'{user_char_name} -- you have already added a callout for {date_of_callout} with reason: {reason}')
    except INVALIDDATETIMEFORMAT:
        await interaction.response.send_message(f'{user_char_name} -- please format the date as one of the following: \nYYYY-MM-DD \nMM-DD-YYYY \nYYYYMMDD')
    except FOREIGNKEYVIOLATION:
        await interaction.response.send_message(f'{user_nick} -- please register with the bot using the following command!\n`/registercharacter`\n Please use your in-game name!')
    except helper.db_helper.DateTimeError:
        await interaction.response.send_message(f'{user_nick}, you\'re trying to submit a callout for a time in the past! Please verify that this is what you want to do!')
    except psycopg2.Error as e:
        await interaction.response.send_message(f'{user_nick} -- an error has occured!\nNotifying <@{CONTRASTELLAR}> of this error. Error is as follows --\n{e}')
    else:
        await interaction.response.send_message(f'{user_char_name} -- you added a callout for {date_of_callout} with reason: {reason}')


@client.tree.command()
async def remove_callout(interaction: discord.Interaction, date_of_callout: str) -> None:
    delete_invalidate()
    cleanup_invalidate()
    user_id = interaction.user.id
    user_char_name = DATABASE_CONN.return_char_name(user_id)
    try:
        DATABASE_CONN.remove_callout(user_id=user_id, callout=date_of_callout)
    except psycopg2.Error:
        await interaction.response.send_message(f'{user_char_name} -- you have not added a callout for {date_of_callout}')
    else:
        await interaction.response.send_message(f'{user_char_name} removed a callout for {date_of_callout}')


@client.tree.command()
async def schedule(interaction: discord.Interaction, days: int = DAYS_FOR_CALLOUTS) -> None:
    delete_invalidate()
    cleanup_invalidate()
    interaction.response.defer(thinking=True)
    callouts: list = DATABASE_CONN.query_callouts(days=days)
    callouts: str = DATABASE_CONN.formatted_list_of_callouts(callouts)
    await interaction.followup.send(f'Callouts for the next {days} days:\n{callouts}')
    return


args: argparse.Namespace = parser.parse_args()

# To be used for reading/writing to the database
# #will not handle the parsing of the returns from the db
DATABASE_CONN = helper.db_helper.DBHelper(args.database)


TOKEN: str = open(args.token, encoding='utf-8').read()
client.run(TOKEN)
