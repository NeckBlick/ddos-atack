#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
END='\033[0m'

proxy_config(){
    echo -e "\n\n$GREEN [+] Start building proxy image with stunnel...$END\n\n\n"
    docker build -t privoxy-stunnel -f ./Dockerfile.TOR.Stunnel .

    sleep 1
    echo -e "\n\n$GREEN [+] Starting proxy containers with stunnel...$END\n\n\n"
    
    for i in $(seq 1 5)
    do
        # Iniciar cada container com diferentes portas
        docker run -d --name privoxy_stunnel_$i -p $((8118+$i)):8118 -p $((9050+$i)):9050 -p $((4433+$i)):4433 privoxy-stunnel
        
        # Tempo de espera para garantir que o container foi inicializado
        sleep 2

        echo -e "\n$GREEN[+] Testing stunnel proxy privoxy_stunnel_$i on port $((4433+$i))...$END"

        # Testar se o proxy via stunnel está funcionando corretamente usando curl via HTTPS (port 4433)
        response=$(curl -s -x https://127.0.0.1:$((4433+$i)) --insecure http://ifconfig.es)

        # Verifica se a resposta contém um endereço IP
        if [[ $response =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo -e "$GREEN[+] Proxy privoxy_stunnel_$i (127.0.0.1:$((4433+$i))) is working via stunnel. Public IP: $response$END"
        else
            echo -e "$RED[-] Proxy privoxy_stunnel_$i (127.0.0.1:$((4433+$i))) failed via stunnel. Check the container.$END"
        fi

        sleep 1
    done
}
proxy_config
