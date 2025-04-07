"""
Script que utiliza o modelo de histórico para fazer inserção no aluno selecionado, passar as configurações o arquivo de histórico que foi gerado por insert_escolas preenchido,
e o estudante referente ao histórico
"""

from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import copy
import os
import argparse
from functools import reduce

def convert_historico_id(historico):
    historico['disciplina_id'] = ObjectId(historico['disciplina_id']) 
    return historico


local_path = os.path.dirname(__file__)
print("Local path",local_path)
db_resources_path = os.path.join(local_path, '..', '..', 'db_resources')

# Normalizando o caminho
db_resources_path = os.path.abspath(db_resources_path)

parser = argparse.ArgumentParser(description="Insere historico no banco de dados.")

#Recupera argumentos
parser.add_argument("--record", type=str, default="", help="Historico Escolar")
parser.add_argument("--env", type=str, default="", help="Ambiente")
parser.add_argument("--student", type=str, default="", help="Estudante")

# Carrega configurações
args = parser.parse_args()
f_config = {}
f_config = open('{}/db_config.json'.format(db_resources_path))
mongo_db_infos = json.load(f_config)

mongo_db_infos = mongo_db_infos[args.env]

if 'CLUSTER' not in mongo_db_infos:
    mongo_db_infos['CLUSTER'] = mongo_db_infos['HOST'] + ":" + mongo_db_infos['PORT']

# Connect to the database
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
historico={}
historico_raw={}
with open('{}/data/{}.json'.format(local_path, args.record), "r", encoding="utf-8") as file:
    historico_raw = json.loads(file.read())

historico = historico_raw[0]['historico']

#Recupera escola associada ao estudante
student = args.student
query = {"turmas.alunos.nome": student}
results = []
print(historico)

for key,value in historico.items():

    result = collection.find_one({'turmas.serie':key})

    historico_escolar = value
    # # Atualização para modificar o histórico do aluno específico
    update = {
        "$set": {
            "turmas.$[turma].alunos.$[aluno].notas.historico_escolar": historico_escolar
        }
    }
    # # Opções para identificar o aluno e a turma corretos
    array_filters = [
        {"turma.serie": key},  # Filtra a turma correta
        {"aluno.nome": args.student}  # Filtra o aluno correto
    ]

    # # Executar a atualização
    results.append(collection.update_one(query, update, array_filters=array_filters))

print("Inserção realizada, {}/3 históricos por serie atualizados".format(reduce(lambda acc, result: acc + result.modified_count,results,0)))
