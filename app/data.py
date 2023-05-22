"""
Module containing a Database class to hold the specs of randomized monsters.'''
"""

from os import getenv
# from typing import Optional, Dict
from certifi import where
from dotenv import load_dotenv, find_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    """
    Database class to connect to database and use functions to add
    documents or reset database as well as creating a dataframe
    """
    # load_dotenv(find_dotenv())
    # database = MongoClient(getenv("MONGO_URL"), tlsCAFile=where())["Database"]

    def __init__(self, collection: str):
        load_dotenv(find_dotenv())
        database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Database"]
        self.collection = database[collection]
        self.version = 0

    # We will create a random seed generator that will generate monsters
    def seed(self, amount=1000):
        """
        Inserts a specified number of MonsterLab.Monster objects into the
        Monster collection.
        """
        data = [Monster().to_dict() for _ in range(amount)]
        return self.collection.insert_many(data).acknowledged

    def reset(self):
        # Removing all documents from the collection via delete_many
        self.collection.delete_many({})

    def count(self) -> int:
        # Return the number of docs that are currently present in the collection
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        # Return ALL docs present as a DataFrame list
        return DataFrame(list(self.collection.find({}, {"_id": False})))

    def html_table(self) -> str:
        """
        Converting the Dataframe to and HTML table, If the table is
        empty we'll return none
        """
        return self.dataframe().to_html()

    def get_csv(self):
        self.dataframe().to_csv("app/csv/data.csv", index=False)


if __name__ == '__main__':
    # creating collection
    load_dotenv()
    test = Database('Database')
    test.reset()
    test.seed(3000)
    print(test.count())
    print(test.dataframe())
    print(test.html_table())
