#!/bin/bash
#Shell script to start server
#To run: type ./startServer.sh and the port you want to start a server on in bash terminal
#e.g ./startServer.sh 5050

PORT=$1

python server.py $PORT