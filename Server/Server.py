#!/usr/bin/python3

#ELABORATO DI PROGRAMMAZIONE DI RETI
#TRACCIA N: 2.
#Gruppo composto da: 
#Cognome: Montanari 
#Nome: Nicola 
#Matricola: 0000970119
#Email: nicola.montanari14@studio.unibo.it

#FILE SERVER

from socket import *
import os
from sys import *
import threading

#Function that handles all the commands.
def commands(request, server, address):

    #If the command is "list".
    if request.decode()=="list":
        print("List of files requested by client:")
        files=os.listdir()
        #Send the number of files to the client. ("-1" Because the Server.py file should not be included in the list)
        server.sendto(str(len(files)-1).encode(), address)
        if len(files)>1:
            print("Sending list of files...")
            #Send the files names one by one.
            for file in files:
                if(file!="Server.py"):
                    server.sendto(file.encode(), address)
            print("List of files sent.")
        else:
            print("No files in the server.")

    #If the command is "get".
    elif request.decode().startswith("get"):
        #If the file exists, and is NOT the Server.py file, start the get process.
        if os.path.exists(request.decode().split(" ")[1]) and request.decode().split(" ")[1]!="Server.py":
            server.sendto("exist".encode(), address)
            print("Sending file...")
            file=open(request.decode().split(" ")[1], "rb")
            data=file.read(1024)
            #Sends the file data.
            while data:
                server.sendto(data, address)
                data=file.read(1024)
            #After the file is sent, close the file and end the "get" process.
            file.close()
            print("File sent.")
        else:
            print("File not found.")
            server.sendto("error".encode(), address)

    #If the command is "put".
    elif request.decode().startswith("put"):
        file, address = server.recvfrom(1024)
        print("Receiving file...")
        #Create a new file and set the timeout to 3 seconds.
        file=open(request.decode().split(" ")[1], "wb")
        server.settimeout(3)
        try:
            #While loop that recives the file and write the data in it.
            while True:
                data, address = server.recvfrom(1024)
                file.write(data)
        #After timeout print an end message and end the "put" process.
        except timeout:
            print("File received.")
            print("\n")


#Main function.
if __name__ == "__main__":
    server=socket(AF_INET,SOCK_DGRAM)
    address=('localhost',8069)
    server.bind(address)
    print("Server started")

    #Endless While loop that recives the request from the client. 
    #When a request is received, a new thread is created to handle the request.
    while True:
        server.settimeout(None)
        request,address=server.recvfrom(1024)
        thread=threading.Thread(target=commands,args=(request, server, address,)) 
        thread.start()
        thread.join()
