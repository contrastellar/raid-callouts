"""
requests helper, to facilitate the requests to the fflogs api
"""

import requests
import json

HEADERS = ''

class RequestsHelper():
    """
    Helper class for the raid-callouts bot.
    This class will contain all of the request-related functions for the bot
    """

    __URL = None
    __HEADERS = None
    __TOKEN = None
    __USER = None
    
    def __init__(self, url, token, user):
        self.__URL = url
        self.__HEADERS = HEADERS
        self.__TOKEN = token
        self.__USER = user

    def __del__(self):
        """
        Destructor for the RequestsHelper class
        No need to do anything here
        """
        pass

    def query(self) -> dict:
        """
        FIXME   right now this function is not able to do anything other than 
                a hard coded query
        
        private function to query the fflogs api
        This should only be invoked by the other functions in this class
        """

        url = self.__URL

        payload = "{\"query\":\"query{\\n\\treportData{\\n\\t\\treport(code: \\\"Bc6zDW9GM4bVkthf\\\"){\\n\\t\\t\\tfights{\\n\\t\\t\\t\\tname,\\n\\t\\t\\t\\tencounterID,\\n\\t\\t\\t\\tid\\n\\t\\t\\t}\\n\\t\\t}\\n\\t}\\n}\"}"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; raid-callous/1.0; +https://github.com/contrastellar/raid-callouts)",
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5YmYxOGQ0Yy02ODIwLTQ4Y2MtYTYyYy0zZDhmZTgxMmY2MjgiLCJqdGkiOiJkNjZlYTI5ZjExYTA2ZmVjYzU0YzBiY2Q1ZDYxNjNjOTJiZWUyZGQwZTY1ZWUzMjczMjc3MmI0ZDY3OGE4NGExMjRiNmZhNjQ2ZGE3NzBmMiIsImlhdCI6MTcxNDYxODE1Ni45ODAxNjcsIm5iZiI6MTcxNDYxODE1Ni45ODAxNzIsImV4cCI6MTc0NTcyMjE1Ni45NjMyNTUsInN1YiI6IjE2NjIwOCIsInNjb3BlcyI6WyJ2aWV3LXVzZXItcHJvZmlsZSIsInZpZXctcHJpdmF0ZS1yZXBvcnRzIl19.mLvDVi2VTht581MgOJOOtT8JaNH7EQ_tlULbbHUozE52vC7wNOzrld8mQ3Q5BiyuKdizp005HTLVayliF_p0TrwvWF9l-24HdswOCMaoDa-Mt4B9hRmqXHN6FF8iYHycMVKbHuBgxjs7nLWlTFNaSD8sONbK6lHGxYFnh0WFCptzF1qvYC6GsSnzJV6FgeZoRxUlNmjj4DoujqUgTifYYmTyl8hUoFfsHgP7aQ1GPfNC_EaSQK6xZV8EOdLmkj4yJk9mgtnYazMYz1hEmZDLCEEtXlhun-MQawm8KtpWOXpwretONnagrbcWgSDnFXzRnpCOqPAKSwsF3fby65Gd3-C97OM24na4i6ms4Fb6FDrZNwzLmhbwWe0uHZwkF7FSDvRDkhaOeGDvrqTApl4e0GgTZMyD7mcv9WAsD3k2RVmOe_8KjQkLr-qHhQx9ymjozBCQaIFUoHDB987QtWtw4nx0jGLmK49-zg9IcjtJivnbJBz1hLp4b4C_o15Wls_zN42aEgZnX9bQpBJoUewkzOm-7C8MaxuXYU2Lf-uCP11lyO6uZWDPKnJ5ie1r3-3VhewdsX7Z6ZIP_chpfRoWIB36WTO_ZJDDiZ3EWJoVh8jiO61hZn7pKT7wSwssOyIgiEx5Lmtx_RUEJA_XSO3b2YJ-WymqFDgqw6lNJDdgZEY"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return json.loads(response.text)
        
