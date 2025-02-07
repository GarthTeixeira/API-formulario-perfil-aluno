import json
from dotenv import load_dotenv
import os

# Carrega o arquivo .env localmente
load_dotenv() 

# Função para carregar configurações de um arquivo JSON
def load_config(json_path="db_resources/db_config.json"):
    with open(json_path, "r") as file:
        config = json.load(file)[os.getenv("FLASK_ENV")]

    # Sobrescrever variáveis com valores do ambiente, se definidos
    host = os.getenv("HOST", config["HOST"])
    port = os.getenv("PORT", config["PORT"])

    config["CLUSTER"] = os.getenv("CLUSTER",host+":"+port)
    config["SRV"] = os.getenv("SRV", config["SRV"])
    config["USER"] = os.getenv("USER", config["USER"])
    config["PASSWORD"] = os.getenv("PASSWORD", config["PASSWORD"])
    config["DB_NAME"] = os.getenv("DB_NAME", config["DB_NAME"])
    config["PARAMS"] = os.getenv("PARAMS", config["PARAMS"])

    return config

