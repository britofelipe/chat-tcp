import threading
import socket

HOST = '127.0.0.1'
PORT = 55123

server = socket.socket(socket.AF_INET)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []
        

def is_command(message, command, size = 0):
    if '/' in message[0]:    
        if command in message[0:10]:
            return True

# BROADCAST: Sends message to all clients
def broadcast(message, client):
    if type(message) != type('a'):
        message = str(message, 'ascii')
    for user in clients:
        if user != client:
            user.send(message.encode('ascii'))

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            message = str(message, 'ascii')

            #/NICK new_nick
            if is_command(message, '/NICK', 5):
                new_nick = message[6:]
                index = clients.index(client)
                client.send(f"Nickname changed to {new_nick}".encode('ascii'))
                broadcast(f'{nicknames[index]} has changed to {new_nick}', client)
                nicknames[index] = new_nick
            
            elif is_command(message, '/USUARIOS', 9):
                try:
                    message = ','.join(nicknames)
                    client.send(message.encode('ascii'))
                except:
                    print('Connection Error')
                    
            elif is_command(message, '/SAIR'):
                try:
                    message = 'Exiting|'
                    client.send(message.encode('ascii'))
                    index = clients.index(client)
                    # Remove client
                    clients.remove(client)
                    client.close()
                    # Remove nickname
                    nickname = nicknames[index]
                    broadcast(f'{nickname} left the chat'.encode('ascii'), client)
                    nicknames.remove(nickname)
                    break
                except:
                    print('Connection Error')
            else:
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
        
        #RECUSAR SE TIVERMOS MAIS DE 4 CLIENTES 
        tamanho = 0
        if tamanho >= 2:
            client.send("REFUSE SIZE".encode('ascii'))
            client.close()
            break    
        
        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024)
        nickname = str(nickname, 'ascii')
        
        
        #SOLICITAR NOVO NICK SE JÁ HOUVER UM USUÁRIO COM UM IGUAL
        if len(nicknames) > 0:
            for nick in nicknames:
                if nickname == nick:
                    client.send("REFUSE NICK".encode('ascii'))
                    nickname = client.recv(1024).decode('ascii') 
                    
        nicknames.append(nickname)
        clients.append(client)
        tamanho += 1

        print(f'Nickname of the client is {nickname}')
        join = f'{nickname} joined the chat|.'.encode('ascii')
        broadcast(join , client)
        client.send('Connected to the server|'.encode('ascii'))

        # We need to process multiple messages at a time
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print(f"Server is listening at port {PORT}")
receive()