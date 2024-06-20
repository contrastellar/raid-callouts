"""
The helper core of the raid-callouts bot.
This module(s) will contain all of the helper functions for the bot

@author: Gabriella 'contrastellar' Agathon
"""

import psycopg2
from configparser import ConfigParser


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

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def connect_config(config: dict) -> psycopg2.connect:
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    

class DBHelper():
    """
    The helper class for the raid-callouts bot.
    This class will contain all of the helper functions for the bot
    """
    
    __CONN: psycopg2.connect = None

    def __init__(self, filename: str, section: str) -> None:
        _config = load_config(filename=filename, section=section)
        self.__CONN = connect_config(_config)

    def __init__(self, filename: str) -> None:
        _config = load_config(filename = filename)
        self.__CONN = connect_config(_config)

    def __init__(self, section: str) -> None:
        _config = load_config(section = section)
        self.__CONN = connect_config(_config)

    def __init__(self) -> None:
        _config = load_config()
        self.__CONN = connect_config(_config)

    def __del__(self):
        """
        Destructor for the DBHelper class
        No need to do anything here
        """
        pass
    
