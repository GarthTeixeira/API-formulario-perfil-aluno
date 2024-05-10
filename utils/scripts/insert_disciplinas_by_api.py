from pymongo import MongoClient
from urllib.parse import quote_plus
import json

f_config = open('../../db_resources/db_config.json')
mongo_db_infos = json.load(f_config)


connection_string = 'mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority&appName=Cluster0&ssl=true'.format(
            mongo_db_infos['USERNAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['HOST']
        )

f_disciplinas = open('../mock/disciplinas.json')
# Connect to the database
client = MongoClient(connection_string)
db = client['competencias_enem_data']
collection = db['escolas']

nome_da_escola = 'third_school'
disciplinas = json.load(f_disciplinas)

# Define the data to be inserted
data = {
    'name': nome_da_escola,
    'disciplinas': disciplinas
}

# Insert the data into the collection
collection.insert_one(data)

# Close the MongoDB connection
client.close()