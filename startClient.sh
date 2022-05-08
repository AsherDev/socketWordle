#!/bin/bash
#Shell script to start client
#To run: type ./startClient.sh followed by the ip address and port number of the server you want to connect to into UNIX terminal
#e.g ./startClient.sh 129.180.124.29 5050
#You can find the ip address of the server by looking at the output of startServer.sh

HOST=$1
PORT=$2

python client.py $HOST, $PORT