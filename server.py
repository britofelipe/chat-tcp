import threading
import socket

HOST = '127.0.0.1'
PORT = 55124

server = socket.socket(socket.AF_INET)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def is_command(message, command, size):
    print(f'message to decode: {message}')
    if '/' in message[0]:    
        if command in message[0:10]:
            return True

# BROADCAST: Sends message to all clients
def broadcast(message, client):
    message = str(message, 'ascii')
    for user in clients:
        if user != client:
            user.send(message.encode('ascii'))

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(type(message))
            message = str(message, 'ascii')

            #/NICK new_nick
            if is_command(message, '/NICK', 5):
                new_nick = message[6:]
                index = nicknames.index(nickname)
                broadcast(f'{nickname} has changed to {new_nick}')
                nickname = new_nick
                nicknames[index] = nickname
            
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