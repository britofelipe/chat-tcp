import threading
import socket

host = '127.0.0.1'
port = 55123

server = socket.socket(socket.AF_INET)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# BROADCAST: Sends message to client
def broadcast(message):
    for client in clients:
        client.send(message)

