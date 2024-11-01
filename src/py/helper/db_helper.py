"""
The helper core of the raid-callouts bot.
This module(s) will contain all of the helper functions for the bot

@author: Gabriella 'contrastellar' Agathon
"""

import psycopg2
import psycopg2.extensions
from configparser import ConfigParser
import datetime


def load_config(filename='database.ini', section='postgresql'):
    """
    Args:
        filename (str, optional): filename for the ini file. Defaults to 'database.ini'.
        section (str, optional): defines the section for the ini file to read from. Defaults to 'postgresql'.

    Raises:
        Exception: Will raise an exception if the postgresql section is not found in the ini file.

    Returns:
        dict: A dictionary containing the parsed values from the ini file, to be used for the database connection.
    """
    parser = ConfigParser()
    parser.read(filename)

    # get section, default is postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    
    return config

def connect_config(config) -> psycopg2.extensions.connection:
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
        
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn is None:
            raise psycopg2.DatabaseError('Failed to connect to the PostgreSQL database')
    

class DBHelper():
    """
    The helper class for the raid-callouts bot.
    This class will contain all of the helper functions for the bot
    """
    
    __CONN: psycopg2.extensions.connection = None

    def __init__(self, filename = 'database.ini', section = 'postgresql') -> None:
        _config = load_config(filename=filename, section=section)
        self.__CONN = connect_config(_config)
        self.__CONN.autocommit = True


    def __del__(self):
        """
        Destructor for the DBHelper class
        No need to do anything here
        """
        # self.__CONN.close()
        pass


    def query_callouts(self, days: int) -> list:
        """This function will query the database for the callouts for the next X days, where X is defined by the days parameter.

        Args:
            days int: number of days in the future to query for callouts

        Returns:
            list: list of users + their callouts for the next X days
        """
        cursor = self.__CONN.cursor()
        # Weird query, but it grabs the callouts from the last day to the next X days.
        cursor.execute(f"SELECT * FROM callouts WHERE date >= NOW() - INTERVAL '1 day' AND date <= NOW() + INTERVAL '{days} days' ORDER BY date ASC;")
        self.__CONN.commit()

        return cursor.fetchall()
    

    def add_callout(self, user_id: int, callout: datetime.date, reason: str, nickname: str) -> None:
        """Add a callout to the database

        Args:
            user_id (int): the Discord UUID of the user adding things to the db
            callout (datetime.date): The day of the callout
            reason (str): The reason of the callout
            nickname (str): The server(guild) nickname of the user who is making the callout
        """
        cursor = self.__CONN.cursor()

        cursor.execute("INSERT INTO callouts (user_id, date, reason, nickname) VALUES (%s, %s, %s, %s)", (user_id, callout, reason, nickname))
        self.__CONN.commit()

        return
    

    def remove_callout(self, user_id: int, callout: datetime.datetime) -> None:
        """Remove a callout based on user + date, which form the primary key in the db

        Args:
            user_id (int): The Discord UUID of the user removing something from the db
            callout (datetime.datetime): The date of the callout
        """
        cursor = self.__CONN.cursor()

        cursor.execute("DELETE FROM callouts WHERE user_id = %s AND date = %s", (user_id, callout))
        self.__CONN.commit()

        return
    
    def formatted_list_of_callouts(self, callouts: list) -> str:

        length = len(callouts)
        output: str = ''

        # Quick and dirty way to say that there were no callouts found during the query
        if length == 0:
            return 'No callouts found for the requested timeframe'
        
        for entry in callouts:
            
            # this is a bit wonky, but we take the known constant width of each entry (4 columns)
            # then we use python's range function to turn "item" into an interator
            # Then we do some funky logic on the entry that we're iterating over
            # in order to get the proper formatting 
            for item in range(4):
                if item == 0:
                    # skip discord user ID always
                    continue

                elif item == 1:
                    # handles the date displaying logic
                    if datetime.date.today() == entry[1]:
                        output += 'TODAY -- '
                    else:
                        output += f'{entry[1]} -- '

                elif item  == 2:
                    # in the database, this is actually the "reason" place
                    # instead of doing that, we call the last column's value
                    # which is the nickname
                    # this was requested by Yasu
                    output += entry[3] + ' -- '

                elif item == 3:
                    # Finally add the reason for the user's callout
                    # two line breaks as Yasu requested
                    output += entry[2] + "\n---\n"

        return output
    
    def format_list_of_callouts(self, callouts: list) -> str:
        """Format the python list of callouts.

        Args:
            callouts (list): The list that needs to be formatted

        Returns:
            str: The formatted list
        """
        raise DeprecationWarning("This method has been deprecated.")
        length = len(callouts)
        output = ''
        if length == 0:
            return 'No callouts found for the requested timeframe'
        
        for entry in callouts:
            # Using basic for-loop logic
            # Entry is the first "dimension" of the list, 
            # Item is the second dimension
            # Because we use "for" in line 148, we don't need
            # to worry about looping or counting
            #
            #
            # This follows the order of columns in the database
            # UID, Date, Reason, Nickname
            i: int = 0  # counter for second dimension, to keep track of things,
                        # and enable 'skipping' of the user_id column
            for item in entry:
                if i == 0:
                    # !!ALWAYS Skip the user_id column
                    i += 1
                    continue
                elif i == 1:
                    # Format the "date" line depending on if 
                    # the callout is occuring today or not
                    if datetime.date.today() == item:
                        output += 'TODAY -- '
                    else:
                        output += f'{item} -- '

                elif i == 2:
                    # Append the "Reason" line
                    output += f'{item} -- '
                else:
                    # Finally, append the nickname at the very end
                    output += f'{item}\n'
                i += 1

        return output
