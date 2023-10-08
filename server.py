import threading
import socket

HOST = '127.0.0.1'
PORT = 55123
MAX_USERS = 4

server = socket.socket(socket.AF_INET)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

commands = {
    '/JOIN',
    '/NICK',
    '/USERS',
    '/EXIT'
}

# BROADCAST: Sends message to client
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def send_users(client):
    users = 'Connected users: ' + ', '.join(nicknames)
    client.send(users.encode('ascii'))

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            if (message in commands):
                if(message == '/JOIN'):
                    client.send("You are already in the server! Did you mean '/EXIT'?".encode('ascii'))
                elif message == '/USERS':
                    send_users(client)
            broadcast(message, client)
        except:
            index = clients.index(client)
            # Remove client
            clients.remove(client)
            client.close()
            # Remove nickname
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'), client)
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # Accept clients all the time
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat|'.encode('ascii'), client)
        client.send('Connected to the server| '.encode('ascii'))
        client.send('Write your first message: '.encode('ascii'))

        # We need to process multiple messages at a time
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print(f"Server is listening at port {PORT}")
receive()