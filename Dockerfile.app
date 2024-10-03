# Use uma imagem base que tenha o suporte para instalar pacotes
FROM debian:bullseye

# Atualizar pacotes e instalar Tor e Privoxy
RUN apt-get update && \
    apt-get install -y tor privoxy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar o Privoxy para usar o Tor
RUN echo "listen-address  0.0.0.0:8118\nforward-socks5t / 127.0.0.1:9050 ." >> /etc/privoxy/config

# Expor as portas necessárias
EXPOSE 8118 9050

# Iniciar Tor e Privoxy
CMD service tor start && privoxy /etc/privoxy/config