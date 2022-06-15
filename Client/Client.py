#!/usr/bin/python3

#ELABORATO DI PROGRAMMAZIONE DI RETI
#TRACCIA N: 2.
#Gruppo composto da: 
#Cognome: Montanari 
#Nome: Nicola 
#Matricola: 0000970119
#Email: nicola.montanari14@studio.unibo.it

#FILE CLIENT

from socket import *
from os.path import *
import os
from sys import *

#Function that handles the "list" command.
def list(client):
    print("List of files:")
    #Recive the number of files on the server.
    files, address = client.recvfrom(1024)
    #If there are no files on the server, print a message and end the function.
    if files.decode()=="0":
        print("No files in the server")
    else:
        #Set timeout to 3 seconds. (The cycle ends after no data has been received for 3 seconds)
        client.settimeout(3)
        try:
            #While loop that recives the files name one by one.
            while True:
                files, address = client.recvfrom(1024)
                #Print the files names.
                print(files.decode())
        except timeout:
            #After timeout print an end message and end the function.
            print("\n")              


#Function that handles the "get" command.
def get(client, request):
    print("Getting file...")
    #Recive the a response from the server (if the file exists or not).
    file, address = client.recvfrom(1024)
    #If the file does not exist, print a message and end the function.
    if file.decode()!="exist":
        print("File not found")
    else:
        print("Receiving file...")
        #Create a new file and set the timeout to 3 seconds.
        file=open(request.split(" ")[1], "wb")
        client.settimeout(3)
        try:
            #While loop that recives the file and write the data in it.
            while True:
                data, address = client.recvfrom(1024)
                file.write(data)
        except timeout:
            #After timeout print an end message and end the function.
            print("File received.")
            print("\n")

#Function that handles the "put" command.
def put(client, file, address):
    #If the file exists, and is NOT the Client.py file, start the put process.
    if os.path.isfile(file.split(" ")[1]) and file.split(" ")[1]!="Client.py":
        client.sendto(file.encode(), address)
        client.sendto("exist".encode(), address)
        print("Sending file...")
        #Open the file and read the data.
        file=open(file.split(" ")[1], "rb")
        data=file.read(1024)
        #While loop that sends and read the data until the end of the file.
        while data:
            client.sendto(data, address)
            data=file.read(1024)
        #After the file is sent, close the file, print an end message and end the function.
        file.close()
        print("File sent.")
    else:
        print("File not found.")


#Main function
if __name__ == "__main__":
    address=('localhost',8069)
    client=socket(AF_INET,SOCK_DGRAM)

    #Endless while loop that handles the client's commands. Only ends when the user types "exit".
    while True:
        #Disable timeout. (Some function could set the timeout)
        client.settimeout(None)
        #Create an input request asking the user to insert a command.
        request=input("Enter your request: ")

        #If the request is "exit", break the loop, print an end message and close the program.
        if request=="exit":
            break

        #If the request is "list", send the request to the server and call the function that handles the "list" command.
        elif request=="list":
            client.sendto(request.encode(), address)
            list(client)

        #If the request is "get", send the request to the server and call the function that handles the "get" command.
        elif request.startswith("get"):
            client.sendto(request.encode(), address)
            get(client, request)

        #If the request is "put", send the request to the server and call the function that handles the "put" command.
        elif request.startswith("put"):
            put(client, request, address)

    print("Closing client...")
    exit(0)    