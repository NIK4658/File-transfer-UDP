#!/usr/bin/python3

from socket import *
import os
from sys import *
import threading

def commands(request, server, address):
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

    elif request.decode().startswith("get"):
        print("File requested by client:")
        file=request.decode().split(" ")[1]
        if os.path.isfile(file):
            server.sendto("exist".encode(), address)
            print("Sending file...")
            with open(file, "rb") as f:
                for line in f:
                    server.sendto(line, address)
                server.sendto("".encode(), address)
            print("File sent.")
        else:
            server.sendto("not exist".encode(), address)
            print("File not found.")
    


    elif request.decode().startswith("put"):
        print("Initializing Upload File:")
        file=request.decode().split(" ")[1]
        print("Receiving file...")
        with open(file, "wb") as f:
            while True:
                data=server.recvfrom(1024)
                if data[0]=="":
                    break
                f.write(data[0])
        print("File received.")






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
