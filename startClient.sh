#!/bin/bash
#Shell script to start client
#To run: type ./startClient.sh followed by the ip address and port number of the server you want to connect to into UNIX terminal
#e.g ./startClient.sh 0.0.0.0 5050
#The server now listens on all interfaces
#You can find the ip address of the server by looking at the output of startServer.sh

HOST=$1
PORT=$2

python client.py $HOST, $PORT