from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import copy
from faker import Faker
import os
import argparse

#Caminho Local
local_path = os.path.dirname(__file__)
print("Local path",local_path)
# Caminho relativo até "db_resources"
db_resources_path = os.path.join(local_path, '..', '..', 'db_resources')
# Normalizando o caminho
db_resources_path = os.path.abspath(db_resources_path)

parser = argparse.ArgumentParser(description="Anonimiza alunos no banco de dados.")
parser.add_argument("--env", type=str, default="", help="ambiente")

# Parse dos argumentos
args = parser.parse_args()
f_config = {}

f_config = open('{}/db_config.json'.format(db_resources_path))
mongo_db_infos = json.load(f_config)

mongo_db_infos = mongo_db_infos[args.env]

if 'CLUSTER' not in mongo_db_infos:
    mongo_db_infos['CLUSTER'] = mongo_db_infos['HOST'] + ":" + mongo_db_infos['PORT']

connection_string = 'mongodb{}://{}:{}@{}/{}'.format(
            mongo_db_infos['SRV'],
            mongo_db_infos['USER_NAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['CLUSTER'],
            mongo_db_infos['PARAMS']
        )

client = MongoClient(connection_string)
db = client['competencias_enem_data']
collection = db['escolas']

# Inicializando o Faker
fake = Faker()

# Passo 1: Coletar nomes únicos dos alunos
aggregation = [
    {
        '$unwind': '$turmas'
    },
    {
        '$replaceRoot': {
            'newRoot': '$turmas'
        }
    }, {
        '$unwind': '$alunos'
    }, {
        '$replaceRoot': {
            'newRoot': '$alunos'
        }
    }, {
        '$group': {
            '_id': '$nome'
        }
    }
]

# Buscar todos os documentos e coletar os nomes dos alunos
documentos = list(collection.aggregate(aggregation))
nomes_unicos = list(map(lambda doc: doc['_id'],documentos))

# Passo 2: Criar um mapeamento de nomes antigos para novos nomes
mapeamento_nomes = {nome_antigo: fake.name() for nome_antigo in nomes_unicos}

print(mapeamento_nomes.items())

# Passo 3: Atualizar os documentos em massa
for nome_antigo, novo_nome in mapeamento_nomes.items():
    # Atualizar todos os documentos onde o nome do aluno aparece
    collection.update_many(
        { "turmas.alunos.nome": nome_antigo },  # Filtro para encontrar documentos com o nome antigo
        { "$set": { "turmas.$[].alunos.$[aluno].nome": novo_nome } },  # Atualização do nome para todas as turmas (turmas$[]) em alunos específicosc ($[aluno])
        array_filters=[{ "aluno.nome": nome_antigo }]  # Filtro para identificar o aluno
    )

    # Exibir o resultado
    print(f"Todos os alunos com nome '{nome_antigo}' atualizados para '{novo_nome}'")

print("Atualização concluída!")
