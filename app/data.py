import os.path
from os import getenv

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    """Database class to connect to database and use functions to add
    documents or reset database as well as creating a dataframe"""
    # connect to database
    load_dotenv()
    database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Database"]

    # directory = os.path.join("app", "csv")

    def __init__(self, collection: str):
        """creates collection in database"""
        self.collection = self.database[collection]

    def seed(self, amount: int) -> str:
        """inserts the specified number of documents into the collection"""
        self.collection.insert_many(Monster().to_dict() for _ in range(amount))

    def reset(self) -> str:
        """deletes all documents from the collection"""
        self.collection.delete_many({})

    def count(self) -> int:
        """returns the number of documents in the collection"""
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        """returns a DataFrame containing all documents in the collection"""
        return DataFrame(self.collection.find({}, {"_id": False}))

    def html_table(self) -> str:
        """returns an HTML table representation
        of the DataFrame, or None if the collection is empty"""
        return self.dataframe().to_html() if self.count() else None

    def get_csv(self):
        """creates a csv of the DataFrame"""
        self.dataframe().to_csv("app/csv/data.csv", index=False)


if __name__ == '__main__':
    # creating collection
    db = Database('Bandersnatch')
