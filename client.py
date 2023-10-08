import socket
import threading

entry = ''
while(entry != "/JOIN"):
    entry = input("Please write /JOIN to enter the chat: ")
    if(entry == "/JOIN"):
        break

host = input("Please enter your HOST: ")
port = int(input("Please enter your PORT: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

nickname = input("Enter a nickname: ")
stop_thread = False

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        text = input("You: ")

        if(text == '/JOIN'):
            message = '/JOIN'
            client.send(message.encode('ascii'))
        elif(text == '/NICK'):
            message = '/NICK'
            client.send(message.encode('ascii'))
        elif(text == '/USERS'):
            message = '/USERS'
            client.send(message.encode('ascii'))
        elif(text == '/EXIT'):
            message = '/EXIT'
            client.send(message.encode('ascii'))
        else: 
            message = f'{nickname}: {text}'
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
