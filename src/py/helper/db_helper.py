"""
The helper core of the raid-callouts bot.
This module(s) will contain all of the helper functions for the bot

@author: Gabriella 'contrastellar' Agathon
"""

import psycopg2

class DBHelper():
    """
    The helper class for the raid-callouts bot.
    This class will contain all of the helper functions for the bot
    """
    
    __CONN = None
    __DB_USER = None
    __DB_PASS = None

    def __init__(self, db_url, db_user, db_pass):
        self.__CONN = psycopg2.connect(db_url, db_user, db_pass)
        self.__DB_USER = db_user
        self.__DB_PASS = db_pass
    
    def __del__(self):
        self.__CONN.close()
