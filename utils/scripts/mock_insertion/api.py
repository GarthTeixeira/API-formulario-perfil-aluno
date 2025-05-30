import requests
import asyncio
import aiohttp

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