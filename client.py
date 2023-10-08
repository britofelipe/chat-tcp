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
                message = client.recv(1024).decode('ascii')
                print("All ready, type anything to the chat")
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
        text = input("You: ")
        sendMessage = f'{nickname}: {text}'
        client.send(sendMessage.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

