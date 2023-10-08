import threading
import socket

HOST = '127.0.0.1'
PORT = 55123

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

# HANDLE: Handle messages from client
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            if message.split(": ")[1] in commands:
                command = message.split(": ")[1]
                if (command == '/JOIN'):
                    client.send("You are already in the server! Did you mean '/EXIT'?")
                elif command.startswith('/NICK'):
                    if(len(clients) >= 4):
                        client.send("REFUSE SIZE".encode('ascii'))
                        client.close()
                    else:
                        try:
                            new_nick = message.split()[1]
                            index = clients.index(client)
                            old_nick = nicknames[index]
                            nicknames[index] = new_nick
                            client.send(f"Nickname changed to {new_nick}".encode('ascii'))
                            broadcast(f'{old_nick} has changed to {new_nick}'.encode('ascii'), client)
                        except:
                            print("Failed to change nickname")
                elif (command == '/USERS'): 
                    try: 
                        users_list = ', '.join(nicknames)
                        client.send(users_list.encode('ascii'))
                    except:
                        ("Failed to show all users")
                        break
                elif (command == '/EXIT'): 
                    try:
                        message = 'Exiting|'
                        client.send(message.encode('ascii'))
                        index = clients.index(client)
                        clients.remove(client)
                        client.close()
                        nickname = nicknames[index]
                        broadcast(f'{nickname} left the chat'.encode('ascii'), client)
                        nicknames.remove(nickname)
                        break
                    except:
                        print("Failed to exit properly")
                        break
            else:
                index = nicknames.index(nicknames[clients.index(client)])
                broadcast(f'{nicknames[index]}: {message}'.encode('ascii'), client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
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
        broadcast(f'{nickname} joined the chat'.encode('ascii'), client)
        client.send('Connected to the server|'.encode('ascii'))

        # We need to process multiple messages at a time
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print(f"Server is listening at port {PORT}")
receive()