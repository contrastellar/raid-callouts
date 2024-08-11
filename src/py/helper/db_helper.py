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
    """_summary_

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

    # TODO change this to use default parameters, reducing code bloat
    def __init__(self, filename: str, section: str) -> None:
        _config = load_config(filename=filename, section=section)
        self.__CONN = connect_config(_config)
        self.__CONN.autocommit = True


    def __init__(self, filename: str) -> None:
        _config = load_config(filename = filename)
        self.__CONN = connect_config(_config)
        self.__CONN.autocommit = True


    def __init__(self, section: str) -> None:
        _config = load_config(section = section)
        self.__CONN = connect_config(_config)
        self.__CONN.autocommit = True


    def __init__(self) -> None:
        _config = load_config()
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

        return cursor.fetchall() # No idea if this is actually returning a list
    

    def add_callout(self, user_id: int, callout: datetime.date, reason: str, nickname: str) -> None:
        cursor = self.__CONN.cursor()

        cursor.execute("INSERT INTO callouts (user_id, date, reason, nickname) VALUES (%s, %s, %s, %s)", (user_id, callout, reason, nickname))
        self.__CONN.commit()

        return
    

    def remove_callout(self, user_id: int, callout: datetime.datetime) -> None:
        cursor = self.__CONN.cursor()

        cursor.execute("DELETE FROM callouts WHERE user_id = %s AND date = %s", (user_id, callout))
        self.__CONN.commit()

        return
    
    def format_list_of_callouts(self, callouts: list) -> str:
        length = len(callouts)
        output = ''
        if length == 0:
            return 'No callouts found for the requested timeframe'
        
        for entry in callouts:
            i: int = 0
            for item in entry:
                if i == 0:
                    # Skip the user_id column
                    i += 1
                    continue
                elif i == 1 or i == 2:
                    output += f'{item} -- '
                else:
                    output += f'{item}\n'
                i += 1

        return output
