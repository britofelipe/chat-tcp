import socket
import threading

# entry = ''
# while(entry != "/JOIN"):
#     entry = input("Please write /JOIN to enter the chat: ")
#     if(entry == "/JOIN"):
#         break

# host = input("Please enter your HOST: ")
# port = int(input("Please enter your PORT: "))

host = '127.0.0.1'
port = 55123

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

nickname = input("Enter a nickname: ")
stop_thread = False

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if not message:
                client.close()
                break
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'Exiting|':
                client.close()
                break
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

        text = input("")

        if(text == '/JOIN'):
            message = '/JOIN'
            client.send(message.encode('ascii'))
        elif(text[0:5] == '/NICK'):
            client.send(text.encode('ascii'))
        elif(text == '/USERS'):
            message = '/USERS'
            client.send(message.encode('ascii'))
        elif(text == '/EXIT'):
            try:
                client.send(text.encode('ascii'))
                break
            except:
                print('ERROR: Connection went wrong')
        else: 
            message = f'{nickname}: {text}'
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()