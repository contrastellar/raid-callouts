"""
Database functionality tests.

@author: Gabriella "Contrastellar" Agathon
"""

import datetime
import helper.db_helper

class TestClass():
    """
    Test class for the database functionality.
    These tests should only be assertions of type, not of return values.
    """
    DATABASE_CONN = helper.db_helper.DBHelper("xiv-database.ini")

    def test_add_registration(self) -> None:
        registration = self.DATABASE_CONN.register_char_name(uid=1, char_name="test")
        assert registration is None

    def test_query_callouts(self) -> None:
        callouts = self.DATABASE_CONN.query_callouts(7)
        assert type(callouts) is list

    def test_add_callout(self) -> None:
        callout = self.DATABASE_CONN.add_callout(user_id=1, callout=datetime.date.today(), reason='test', nickname='test', char_name='test')
        assert callout is None
    

    def test_callouts(self) -> None:
        callout = self.DATABASE_CONN.query_callouts(days=7)
        assert callout is not None


    def test_remove_callout(self) -> None:
        remove_callout = self.DATABASE_CONN.remove_callout(user_id=1, callout=datetime.date.today())
        assert remove_callout is None

    def test_char_name(self) -> None:
        char_name = self.DATABASE_CONN.return_char_name(uid=1)
        assert type(char_name) is str
        assert char_name == "test"

    def test_remove_registration(self) -> None:
        registration = self.DATABASE_CONN.remove_registration(uid=1, isOkay=True)
        assert registration is None

    def test_format_list_of_callouts(self) -> None:
        callouts = self.DATABASE_CONN.query_callouts(days=7)
        formatted_callouts = self.DATABASE_CONN.format_list_of_callouts(callouts=callouts)
        assert formatted_callouts.__class__ is str
