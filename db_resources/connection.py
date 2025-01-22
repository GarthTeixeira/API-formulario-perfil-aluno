from pymongo import MongoClient
from urllib.parse import quote_plus
from .load_config import load_config

mongo_db_infos = load_config()

class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = 'mongodb{}://{}:{}@{}:{}/{}'.format(
            mongo_db_infos['SRV'],
            mongo_db_infos['USERNAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['HOST'],
            mongo_db_infos['PORT'],
            mongo_db_infos['PARAMS']
        )
        self.__database_name = mongo_db_infos['DB_NAME']
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        self.__client = MongoClient(self.__connection_string, serverSelectionTimeoutMS=50000)
        self.__db_connection = self.__client[self.__database_name]
        print(self.__client)
        print(self.__db_connection)
   
       
    def close_connection(self):
        self.__client.close()

    def get_db_connection(self):
        return self.__db_connection
    
    def get_db_client(self):
        return self.__client
    
