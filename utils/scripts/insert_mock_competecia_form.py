""" 
O script a seguir funcionam apenas em ambiente local. Para que os dados sejam carregados em produção, realize a importação do ambiente local.
*The following script works only in local environment. To load data in production import from local environment.*

Script de inserção de valores de competência:

Como os resultados dos formulários serão preenchidos por várias pessoas em um longo período de tempo, este script consegue preencher todas
as respostas de professores fakes de todas as disciplinas das turmas.

*
Insertion competence values script:
As the form results are filed by several people over a long period this script can fill in every fake teacher answer from every class subject.
*

"""

from bson.objectid import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import asyncio
import aiohttp
import random
from faker import Faker
import argparse
import time
import requests
import pprint

def put_request(url, payload):
    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP de erro
        return response.json()  # Retorna o JSON da resposta
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def post_request(url, payload):
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP de erro
        return response.json()  # Retorna o JSON da resposta
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

async def put_data(url, session, payload):
    """Faz uma requisição PUT com o payload fornecido."""
    try:
        async with session.put(url, json=payload) as response:
            response.raise_for_status()  # Levanta exceção para status HTTP 4xx/5xx
            return await response.json()  # Retorna a resposta em JSON
    except aiohttp.ClientError as e:
        print(f"Erro ao enviar para {url}: {e}")
        return None

async def put_all(urls_and_payloads):
    """Faz várias requisições PUT em paralelo."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            put_data(url, session, payload)
            for url, payload in urls_and_payloads
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

async def post_data(url, session, payload):
    """Faz uma requisição POST com o payload fornecido."""
    try:
        async with session.post(url, json=payload) as response:
            response.raise_for_status()  # Levanta exceção para status HTTP 4xx/5xx
            return await response.json()  # Converte a resposta para JSON
    except aiohttp.ClientError as e:
        print(f"Erro ao enviar para {url}: {e}")
        return None

async def post_all(urls_and_payloads):
    """Faz várias requisições POST em paralelo."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            post_data(url, session, payload)
            for url, payload in urls_and_payloads
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

parser = argparse.ArgumentParser(description="Cria formularios com valores de competências randômicas.")

parser.add_argument("--school", type=str, default="", help="Id escola")

# Parse dos argumentos
args = parser.parse_args()

f_config = open('/home/garth/Documents/Projetos/API-formulario-perfil-aluno/db_resources/db_config.local.json')
mongo_db_infos = json.load(f_config)


connection_string = 'mongodb{}://{}:{}@{}/{}'.format(
            mongo_db_infos['SRV'],
            mongo_db_infos['USERNAME'],
            quote_plus(mongo_db_infos['PASSWORD']),
            mongo_db_infos['HOST'],
            mongo_db_infos['PARAMS']
        )

url_insert_professor='http://localhost:5000/professor-form/insert-professor'
url_insert_resposta = 'http://localhost:5000/professor-form/insert-resposta'

client = MongoClient(connection_string)
db = client['competencias_enem_data']
competencias_collection = db['competencias']
escolas_collection = db['escolas']

pipeline_num_habilidades = [
    {
        '$project': {
            'descricao_area': 0
        }
    }, {
        '$set': {
            'competencias_habilidades': {
                '$cond': {
                    'if': {
                        '$ne': [
                            '$tag', 'COGNITIVOS'
                        ]
                    }, 
                    'then': {
                        '$size': {
                            '$map': {
                                'input': {
                                    '$objectToArray': '$competencias_habilidades'
                                }, 
                                'as': 'item', 
                                'in': '$$item.k'
                            }
                        }
                    }, 
                    'else': 1
                }
            },
            '_id': {
                '$toString':'$_id'
            }
        }
    }
]

pipeline_turmas = [
    {
        '$match': {
            '_id': ObjectId(args.school)
        }
    }, {
        '$project': {
            'turmas.alunos': 0, 
            'disciplinas': 0, 
            '_id': 0, 
            'name': 0
        }
    }, {
        '$unwind': {
            'path': '$turmas'
        }
    }, {
        '$replaceRoot': {
            'newRoot': '$turmas'
        }
    }, {
        '$set':{
            '_id':  {
                '$toString': '$_id'
            },
            'serie_ano':{ '$toInt': { '$substrCP': ["$serie", 0, 1] } }
        }
    }

]

pipeline_disciplinas = [
    {
        '$match': {
            '_id': ObjectId(args.school)
        }
    }, {
        '$project': {
            'disciplinas': 1
        }
    }, {
        '$unwind': {
            'path': '$disciplinas'
        }
    }, {
        '$replaceRoot': {
            'newRoot': '$disciplinas'
        }
    }, {
        '$set': {
            '_id': {
                '$toString': '$_id'
            }
        }
    }, {
        '$project': {
            'codigoBNCC': 0
        }
    }
]

list_competencias =  list(competencias_collection.aggregate(pipeline_num_habilidades))
list_turmas = list(escolas_collection.aggregate(pipeline_turmas))
list_disciplinas = list(escolas_collection.aggregate(pipeline_disciplinas))


form_ids = []
turma_form_dict = {}

for turma in list_turmas:
    payload = {
        'nome': Faker().name(),
        'email': Faker().email(),
        'escola': args.school,
        'turma': turma
    }
    response = post_request(url_insert_professor,payload)
    print(response)
    turma_form_dict[response['id']] = turma


def insert_resposta():
    print("Getting teatchers")
    formularios = turma_form_dict.keys()

    insert_resposta_url_and_payloads = []
    response = []
    form_num = len(formularios)

    print("{} formularios encontrados".format(form_num))

    for index,formulario in enumerate(formularios):

        serie_da_turma = turma_form_dict[formulario]['serie_ano']
        
        disciplinas_da_turma = list(filter(lambda disc: disc['serie_ano'] == serie_da_turma, list_disciplinas))
        competencias_cognitivas = list(filter(lambda comp: comp['tag']== 'COGNITIVOS', list_competencias))

        for disciplina in disciplinas_da_turma:
            competencias_by_area = list(filter(lambda comp: comp['tag'] == disciplina['area'], list_competencias))
            

            comp_map = {}

            for comp in competencias_by_area:
                comp_map[comp['_id']] = [random.uniform(0, 10) for _ in range(comp['competencias_habilidades'])]
            
            
            payload = {
                'disciplina': disciplina['_id'],
                'professor': formulario,
                'area': disciplina['area'],
                'competencias':comp_map
            }

            nome_diciplina = disciplina["name"] + '-' + str(disciplina["serie_ano"])

            print('formulario {} referente a disciplina {} possui {} competencias'.format(payload['professor'],nome_diciplina, len(comp_map.values())))

            insert_resposta_url_and_payloads.append(
                (url_insert_resposta,payload.copy())
            )

            cog_map = {}
            for comp in competencias_cognitivas:
                cog_map[comp['_id']] = [random.uniform(0, 10)]

            payload['area'] = 'COGNITIVOS'
            payload['competencias'] = cog_map


            insert_resposta_url_and_payloads.append(
                (url_insert_resposta,payload.copy())
            )


        print("Inserting {} answers to form {}/{}".format(len(insert_resposta_url_and_payloads),index +1 ,form_num))

        for url,request in insert_resposta_url_and_payloads:            
            response.append(put_request(url, request))
    
    return response

insert_resposta()