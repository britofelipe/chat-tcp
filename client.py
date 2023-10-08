import socket
import threading

nickname = input("Enter a nickname: ")
stop_thread = False
message = ''

recvID = 0
wrtID = 0
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55124))

def is_command(message, command, size = 0):
    if '/' in message[0]:    
        if command in message[0:10]:
            return True

def receive():
    global stop_thread
    global message
    while True:
        
        try:
            message = client.recv(1024)
            if not message:
                client.close()
                break
            message = str(message, 'ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                message = client.recv(1024).decode('ascii')
                print("All ready, type anything to the chat")
                if message == 'REFUSE NICK':
                    print('Someone with that nickname is already connected, please send another one. Type anything to proceed\n')
                    client.close()
                    # stop_thread = True
                    break
                
            elif message == 'REFUSE SIZE': 
                print('Conection refused, too many users on the server')
                client.close()
                stop_thread = True
                
            elif message == 'Exiting|':
                client.close()
                break
                
            # elif message == 'OK':
            #     pass
            
            else:
                print(message)
        except:     
            print("An error occurred!")
            client.close()
            break

def write():
    global nickname
    global message
    
    while True:
        if stop_thread:
            client.close()
            break
        
        text = input("")
        
        if is_command(text, '/NICK'):
            try:
                if text[5] == " " and text[6] != None:
                    client.send(text.encode('ascii'))
                    nickname = text[6:]
            except IndexError:
                print('ERROR: Faulting characters')
            except:
                print('ERROR: Connection went wrong')
            
        elif is_command(text, '/USUARIOS'):
            try:
                client.send(text.encode('ascii'))
            except:
                print('ERROR: Connection went wrong')
        
        elif is_command(text, '/SAIR'):
            try:
                client.send(text.encode('ascii'))
                while message != 'Exiting|':
                    pass
                print('Got out')
            except:
                print('ERROR: Connection went wrong')
            
        else:
            send = (f'{nickname}: {text}')
            client.send(send.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()


write_thread = threading.Thread(target=write)
write_thread.start()
