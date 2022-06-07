#!/usr/bin/python3

from socket import *
from os.path import *
import os
from sys import *


def list(client):
    print("List of files:")
    files, address = client.recvfrom(1024)
    if files.decode()=="0":
        print("No files in the server")
    else:
        client.settimeout(3)
        try:
            while True:
                files, address = client.recvfrom(1024)
                print(files.decode())
        except timeout:
            print("\n")
                



if __name__ == "__main__":
    address=('localhost',8069)
    client=socket(AF_INET,SOCK_DGRAM)
    eof="".encode()

    while True:
        client.settimeout(None)
        request=input("Enter your request: ")
        if request=="exit":
            break
        elif request=="list":
            client.sendto(request.encode(), address)
            list(client)

        elif request.startswith("get"):
            print("Initializing Download File:")
            file=request.split(" ")[1]
            print("Sending file request...")
            client.sendto(request.encode(), address)
            data, address = client.recvfrom(1024)
            if data.decode()=="exist":
                client.sendto(request.encode(), address)
                with open(file, "wb") as f:
                    while True:
                        data, address = client.recvfrom(1024)
                        if data==eof:
                            break
                        f.write(data)
                print("File received.")
            else:
                print("File not found.")

        
        elif request.startswith("put"):
            print("Initializing Upload File:")
            file=request.split(" ")[1]
            if os.path.isfile(file):
                client.sendto(request.encode(), address)
                print("Sending file...")
                with open(file, "rb") as f:
                    for line in f:
                        client.sendto(line, address)
                    client.sendto("".encode(), address)
                print("File sent.")
            else:
                print("File not found.")

    print("Closing client...")
    exit(0)    