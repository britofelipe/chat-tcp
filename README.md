# chat-tcp

Este código é um servidor e cliente de chat  escrito em Python. O servidor utiliza sockets e threading para lidar com múltiplos clientes. O servidor aceita conexões de clientes, recebe mensagens e as transmite para todos os outros clientes conectados.

## Como funciona o servidor

O servidor começa escutando em um IP e porta específicos. Quando um cliente se conecta, ele é solicitado a fornecer um apelido (nickname). Se o apelido não estiver em uso e o número máximo de usuários não tiver sido atingido, o cliente é adicionado ao chat.

### Comandos disponíveis:

- `/JOIN`: Comando para entrar no servidor
- `/USERS`: Envia a lista de usuários conectados no momento.
- `/NICK <new_nickname>`: Altera o apelido do usuário.
- `/EXIT`: Desconecta o usuário do chat.

## Código e Explicação

### Importações e Configurações Iniciais

```python
import threading
import socket

HOST = '127.0.0.1'  # IP onde o servidor será hospedado
PORT = 55123        # Porta para o servidor escutar
MAX_USERS = 4       # Número máximo de usuários permitidos no chat

server = socket.socket(socket.AF_INET)
server.bind((HOST, PORT))
server.listen()

clients = []    # Lista para armazenar os sockets dos clientes conectados
nicknames = []  # Lista para armazenar os apelidos dos clientes conectados
```

Funções do servidor

#### `broadcast(message, sender)`

Envia uma mensagem para todos os clientes conectados, exceto o remetente.

#### `already_joined(client)`

Notifica o cliente que ele já está no servidor, caso ele escreva /JOIN após logado.

#### `send_users(client)`

Envia a lista de usuários conectados para o cliente solicitante.

#### `close_client(client)`

Fecha a conexão do cliente e notifica os outros usuários.

#### `accept_or_refuse_client(client, nickname)`

Aceita ou recusa a conexão do cliente com base no número de usuários conectados e na disponibilidade do apelido.

#### `change_nick(client, new_nick)`

Altera o apelido do cliente se o novo apelido não estiver em uso.

#### `handle(client)`

Lida com as mensagens recebidas dos clientes e executa comandos específicos com base no conteúdo da mensagem.

#### `receive()`

Aceita novas conexões de clientes e inicia um novo thread para lidar com suas mensagens.

## Client.py

### Visão Geral

Este é um script de cliente em Python para um servidor de chat. Ele permite que o usuário se conecte a um servidor de chat, envie e receba mensagens em tempo real. O script usa sockets e threading para gerenciar a comunicação entre o cliente e o servidor.

### Instruções de Uso

O usuário deve executar o script e seguir as instruções para ingressar no chat. Inicialmente, será solicitado que o usuário insira o comando `/JOIN`, o host e a porta do servidor de chat, e escolha um apelido.

#### Comandos disponíveis:

- `/JOIN`: Usado para ingressar no chat.
- `/NICK <novo_apelido>`: Altera o apelido do usuário.
- `/USERS`: Solicita a lista de usuários conectados no chat.
- `/EXIT`: Sai do chat.

### Código e Explicação

#### Inicialização

O script solicita que o usuário insira o comando `/JOIN`, o host, a porta e um apelido antes de se conectar ao servidor.

```python
entry = ''
while(entry != "/JOIN"):
    entry = input("Please write /JOIN to enter the chat: ")

host = input("Please enter your HOST: ")
port = int(input("Please enter your PORT: "))
nickname = input("Enter a nickname: ")
```

#### Conexão com o Servidor

O cliente se conecta ao servidor usando o host e a porta fornecidos.

```python
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
```

#### Threads de Recebimento e Escrita

Duas threads são iniciadas: uma para receber mensagens do servidor e outra para enviar mensagens para o servidor.

```python
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
```

#### Função receive()

Esta função contínua lê mensagens do servidor e as imprime na tela do cliente. Ela também lida com mensagens especiais, como mudança de apelido e desconexão.

#### Função write()

Permite ao usuário escrever e enviar mensagens para o servidor. Ela também suporta comandos especiais para solicitar a lista de usuários, alterar apelidos e sair do chat.

### Conclusão

Este script de cliente permite que os usuários se conectem a um servidor de chat, enviem e recebam mensagens, e realizem ações especiais, como alterar apelidos e solicitar a lista de usuários conectados. Pode ser expandido e modificado conforme necessário para adicionar funcionalidades adicionais e melhorar a experiência do usuário.