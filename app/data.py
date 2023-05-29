"""
Module containing a Database class to hold the specs of randomized monsters
Pymongo Version < 3.10
"""

from os import getenv
# from typing import Optional, Dict
from certifi import where
from dotenv import load_dotenv, find_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient, collection


class Database:
    """
    Database class that connects to database and uses functions to add
    documents or reset database as well as creating a dataframe.
    """
    load_dotenv(find_dotenv())

    def _collection(self) -> collection:
        """
        Function: Connect to the database and return the relevant collection,
        using .envi file to store credentials with TLS Certificate
        (for security reasons)
        """

        URL = getenv("DB_URL", None)
        NAME = getenv("DB_NAME", None)
        COLLECTION = getenv("DB_COLLECTION", None)

        client = MongoClient(URL,
                             tls=True,
                             tlsCAFile=where())
        return client[NAME][COLLECTION]

    # Function: Create a random seed generator that will generate monsters
    def seed(self, amount: int) -> None:
        """
        Inserts a specified number of MonsterLab.Monster objects into the
        Monster collection.

        Args:
            amount (int): Define the number of Monster objects to insert.
            Goal is at least 1000 monsters.
        """
        if not isinstance(amount, int):
            raise TypeError('''can only use int (not "{}") values for the
                                    amount'''.format(amount.__class__.__name__))

        if amount < 1:
            raise ValueError('amount must be at least 1')

        return self._collection().insert_many(
            Monster().to_dict() for i in range(amount)
        )

    def reset(self):
        # Function: Removing all documents from the collection via .drop method
        return self._collection().drop()

    def count(self) -> int:
        # Function: Return the number of docs that are currently present in the collection
        return self._collection().count_documents({})

    def dataframe(self) -> DataFrame:
        # Function: Create a dataframe object from the whole database.
        return DataFrame(list(self._collection().find({},
                                                      {"_id": False, "Timestamp": False})))

    def html_table(self) -> str:
        """
        Converting the Dataframe to and HTML table, If the table is
        empty we'll return none
        """
        if self.count() > 0:
            return self.dataframe().to_html()
        else:
            return "The collection is empty."


if __name__ == "__main__":
    # Testing the Database Class
    amount = 2048

    db = Database()
    db.reset()
    db.seed(amount)

    count = db.count()
    df = db.dataframe()
    html = db.html_table()

    assert amount == count == df.shape[0]
    assert html is not None