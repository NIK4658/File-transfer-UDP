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


def get(client, request):
    print("Getting file...")
    file, address = client.recvfrom(1024)
    if file.decode()!="exist":
        print("File not found")
    else:
        print("Receiving file...")
        file=open(request.split(" ")[1], "wb")
        client.settimeout(3)
        try:
            while True:
                data, address = client.recvfrom(1024)
                file.write(data)
        except timeout:
            print("File received.")
            print("\n")


def put(client, file, address):
    if os.path.isfile(file.split(" ")[1]) and file.split(" ")[1]!="Client.py":
        client.sendto(file.encode(), address)
        client.sendto("exist".encode(), address)
        print("Sending file...")
        file=open(file.split(" ")[1], "rb")
        data=file.read(1024)
        while data:
            client.sendto(data, address)
            data=file.read(1024)
        file.close()
        print("File sent.")
    else:
        print("File not found.")



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
            client.sendto(request.encode(), address)
            get(client, request)

        elif request.startswith("put"):
            put(client, request, address)

    print("Closing client...")
    exit(0)    