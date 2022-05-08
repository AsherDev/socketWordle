Author: Bryce Watson 220199390
Info: This is my wordle socket project for COSC340 Assignment 2 built using Python.

To run: First start a server by running './startServer.sh' followed by the Port you wish to use. 
For example: ./startServer.sh 5050

Then start a client by running './startClient.sh' followed by the IP Address and Port of your server. You can see the ip address of your server by looking at the [LISTENING] output of startServer.sh in the terminal. 
For example: ./startClient.sh 129.180.124.29 5050

The server interface keeps track of whats happening with connected clients, and the client interface walks the user through a game of wordle.

