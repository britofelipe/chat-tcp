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
    global nickname
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message.startswith('NICKNAME CHANGED TO '):
                new_nick = message[len('NICKNAME CHANGED TO '):].strip('| ')
                nickname = new_nick
                print(f"Your nickname has been changed to {new_nick}")
            elif message == 'EXITING':
                print("You have left the chat.")
                client.close()
                break
            elif message == 'REFUSE SIZE':
                print('Connection refused, too many users on the server.')
                client.close()
                break
            elif message == 'REFUSE NICK':
                print('Connection refused, nickname is already in use.')
                client.close()
                break
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write():
    global nickname
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