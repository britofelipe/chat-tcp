import socket
import threading

nickname = input("Enter a nickname: ")
stop_thread = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55124))

def is_command(message, command):
    
    if message.startswith('/'):
      if message.find(command) != -1:
          return True
      else:
          return False

def receive():
    while True:
        global stop_thread
        try:
            message = client.recv(1024)
            message = str(message, 'ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                message = client.recv(1024).decode('ascii')
                print("All ready, type anything to the chat")
                if message == 'REFUSE NICK':
                    print('Someone with that nickname is already connected, please send another one. Type anything to proceed\n')
                    client.close()
                    stop_thread = True
                
            elif message == 'REFUSE SIZE': 
                print('Conection refused, too many users on the server')
                client.close()
                stop_thread = True
                
            # elif message == 'OK':
            #     pass
            
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
        
        text = input(f"LOCAL: {nickname}: ")
        
        # if is_command(text, '/NICK'):
        # if is_command(text, '/NICK'):
        #     if len(text) > 6 and text[6] == " ":
        #         client.send(text.enconde('ascii'))
            
        # elif is_command(text, '/USUARIOS'):
        
        # elif is_command(text, '/SAIR'):
            
        # else:    
            #message = f'{nickname}: {text}'
        message = (f'{nickname}: {text}')
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
