import socket
import threading

nickname = input("Enter a nickname: ")
stop_thread = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55123))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                message = client.recv(1024).decode('ascii')
                print("All ready, type anything to the chat")
                if message == 'REFUSE NICK':
                    print('Someone with that nickname is already connected, please send another one. Type anything to proceed\n')
                    new_nickname = input("Enter a new nickname: ")
                    while new_nickname == nickname:
                        if nickname != new_nickname:
                            client.send(nickname.encode('ascii'))
                        else:
                            print("Nickname must be diferent than the one you wrote previously")
                            new_nickname = input("Enter a new nickname: ")

                
            elif message == 'REFUSE SIZE': 
                print('Conection refused, too many users on the server')
                client.close()
                stopThread = True
                
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            client.close()
            break
        
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
