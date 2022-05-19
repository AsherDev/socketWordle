import socket
import sys
from Crypto.Cipher import AES
import binascii, os


#Size of messages
HEADER = 64
#Port is provided by shell script argument, provide error on invalid argument
try:
    PORT= int(sys.argv[2])
except:
    print("ERROR: Please provide a valid IP address and Port number; see readme for help")
    exit(0)
#Character encoding format
FORMAT = 'utf-8'
#Message to disconnect from server
DISCONNECT_MESSAGE = "DISCONNECT"
#Message to start game
STARTGAME_MESSAGE = "START GAME"
#Message to end game
GAMEOVER_MESSAGE = "GAME OVER"
#Host is provided by shell script argument, provide error on invalid argument
try:
    HOST = sys.argv[1]
except:
    print("ERROR: Please provide a valid IP address and Port number; see readme for help")
    exit(0)
#sys.argv[] adds a comma to the end of the string for some reason, so replace them with empty strings
HOST = HOST.replace(',','')
#Tuple with host ip and port number of the server you want to attempt to connect to
ADDRESS = (HOST, PORT)
#Create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to server, produce error on failure
try:
    client.connect(ADDRESS)
except:
    print("ERROR: Unable to connect to server; please check you have the correct IP address and Port number.")
    exit(0)

#Initialization vector is random 16bytes
iv = os.urandom(16)
#Shared encryption key with server
key = b"Sixteen byte key"

#Function to encrypt messages
def encrypt(data, key, iv):
    plaintext = data
    plaintext += b' ' * (16 - len(plaintext) % 16)
    

    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(plaintext)

#Function to decrypt messages
def decrypt(data, key, iv):
 
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    return cipher.decrypt(data)

#Function to send a message to the server
def send(msg):
    
    message = msg.encode(FORMAT)
    client.send(iv)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    encrypted_message = encrypt(message, key, iv)
    client.send(encrypted_message)



#main function that guides the user through a game of wordle after connecting to the server and establishing a game
def main():
    send(STARTGAME_MESSAGE) 
    #run forever  
    while True: 
        #expect messages
        message = client.recv(16)
        if message:
            message = decrypt(message, key, iv)
            message = message.decode(FORMAT).strip()
            
            #If the client recieves the disconnect message for whatever reason, close the connection and exit
            if message == DISCONNECT_MESSAGE:
                print("Connection to the server has been dropped. Exiting...")
                exit(0)
            #if the client recieves the gameover message after winning, close the connection and exit
            elif message == GAMEOVER_MESSAGE:
                message = client.recv(16)
                message = decrypt(message, key, iv)
                message = message.decode(FORMAT).strip()
                print(f"Victory! Game is over. It took you {message} guesses to get the correct word. Exiting...")
                exit(0)
            #"OK" is what the server sends the client as confirmation of the startgame message, upon receving this we start the game by producing texts and prompting the user for a guess
            elif message == "OK":
                print("Wordle game now starting..")
                print("Welcome to Wordle!")
                #Expect the hint message
                message = client.recv(16)
                message = decrypt(message, key, iv)
                message = message.decode(FORMAT).strip()
                print(f"Heres your hint: {message}")
                client_message = str(input("Take a guess: "))
                #If the user decides to instead diconnect, they can type "disconnect" (case insensitive) and the client will close the connection and exit after notifying the server
                if client_message == DISCONNECT_MESSAGE:
                    send(DISCONNECT_MESSAGE)
                    print("Connection to the server has been dropped. Exiting...")
                    exit(0)
                else:
                #If not, nevermind
                    send(client_message)
                    continue
            #If the player guessed a word that either wasn't a 5 character string, and/or the word wasn't on the word guess list, let them know they suck and make them try again
            elif message == "INVALID GUESS":
                print("INVALID WORD; Sorry, that's not gonna work pal")
                client_message = str(input("Try again: "))
                #Again they can choose to discconect
                if client_message == DISCONNECT_MESSAGE:
                    send(DISCONNECT_MESSAGE)
                    print("Connection to the server has been dropped. Exiting...")
                    exit(0)
                else:
                #We aren't quitters here!
                    send(client_message)
                    continue
            #If the player made a valid guess, meaning the word they guessed was a 5 character string, and the word is on the word guess list, throw them a bone and chuck them a hint
            elif message == "VALID GUESS":
                message = client.recv(16)
                message = decrypt(message, key, iv)
                message = message.decode(FORMAT).strip()
                print(f"Heres your hint: {message}")
                client_message = str(input("Take a guess: "))
                #you get the idea
                if client_message == DISCONNECT_MESSAGE:
                    send(DISCONNECT_MESSAGE)
                    print("Connection to the server has been dropped. Exiting...")
                    exit(0)
                #at least, i hope you do
                else:
                    send(client_message)
                    continue
            #If the client recieves any other message, then we let the user know its whack and then close the connection and exit
            else:
                print("Something has gone wrong with the server, Exiting...")
                send(DISCONNECT_MESSAGE)
                exit(0)

                
main()