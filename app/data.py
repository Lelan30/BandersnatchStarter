from os import getenv

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    '''Database class to connect to database and use functions to add
    documents or reset database as well as creating a dataframe'''
    # connect to database
    load_dotenv()
    database = MongoClient(getenv('DB_URL'), tlsCAFile=where())['Database']

    def __init__(self, collection: str):
        '''creates collection in database'''
        self.collection = self.database[collection]

    def seed(self, amount: int) -> str:
        '''inserts the specified number of documents into the collection'''
        docs = [Monster().to_dict() for _ in range(0, amount)]
        self.collection.insert_many(docs)
        print(f'{amount} documents have been added to Database')

    def reset(self) -> str:
        '''deletes all documents from the collection'''
        self.collection.delete_many({})
        print('Database has been reset!')

    def count(self) -> int:
        '''returns the number of documents in the collection'''
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        '''returns a DataFrame containing all documents in the collection'''
        # create cursor to execute query
        cur = self.collection.find({})
        # create dataframe
        data_frame = DataFrame(cur)

        if self.count() <= 0:
            return 'There are no documents in Database'

        # drop _id col
        data_frame = data_frame.drop('_id', axis=1)
        print(f'DataFrame with {self.count()} documents has been created!')
        return data_frame

    def html_table(self) -> str:
        '''returns an HTML table representation
        of the DataFrame, or None if the collection is empty'''
        if self.count() <= 0:
            return 'No documents in database'
        return self.dataframe().to_html()


if __name__ == '__main__':
    # creating collection
    db = Database('Bandersnatch')
