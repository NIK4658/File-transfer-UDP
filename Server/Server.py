#!/usr/bin/python3

from socket import *
import os
from sys import *
import threading

def commands(request, server, address):
    eof="".encode()
    if request.decode()=="list":
        print("List of files requested by client:")
        files=os.listdir()
        server.sendto(str(len(files)-1).encode(), address)
        if len(files)>1:
            print("Sending list of files...")
            for file in files:
                if(file!="Server.py"):
                    server.sendto(file.encode(), address)
            print("List of files sent.")
        else:
            print("No files in the server.")

    elif request.decode().startswith("get"):
        if os.path.exists(request.decode().split(" ")[1]) and request.decode().split(" ")[1]!="Server.py":
            server.sendto("exist".encode(), address)
            print("Sending file...")
            file=open(request.decode().split(" ")[1], "rb")
            data=file.read(1024)
            while data:
                server.sendto(data, address)
                data=file.read(1024)
            file.close()
            print("File sent.")
        else:
            print("File not found.")
            server.sendto("error".encode(), address)

    elif request.decode().startswith("put"):
        file, address = server.recvfrom(1024)
        print("Receiving file...")
        file=open(request.decode().split(" ")[1], "wb")
        server.settimeout(3)
        try:
            while True:
                data, address = server.recvfrom(1024)
                file.write(data)
        except timeout:
            print("File received.")
            print("\n")


if __name__ == "__main__":
    server=socket(AF_INET,SOCK_DGRAM)
    address=('localhost',8069)
    server.bind(address)
    print("Server started")

    while True:
        server.settimeout(None)
        request,address=server.recvfrom(1024)
        thread=threading.Thread(target=commands,args=(request, server, address,)) 
        thread.start()
        thread.join()
