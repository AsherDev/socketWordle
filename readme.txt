Author: Bryce Watson 220199390
Info: This is my wordle socket project for COSC340 Assignment 2/4 built using Python.

To run: First start a server by running './startServer.sh' followed by the Port you wish to use. 
For example: ./startServer.sh 5050

Then start a client by running './startClient.sh' followed by the IP Address 0.0.0.0 and Port of your server. You can see the ip address of your server by looking at the [LISTENING] output of startServer.sh in the terminal. 
For example: ./startClient.sh 0.0.0.0 5050

The server now listens on all interfaces. This is easily configurable by changing the address parameter in the server.py if you want to start the server on the current address.

The server interface keeps track of whats happening with connected clients, and the client interface walks the user through a game of wordle.

