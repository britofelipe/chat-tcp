# chat-tcp
A python implementation of a 4-person chat using tcp

## SERVER.py

### is_command(message, command, size=0)

- Função utilizada para verificar se a mensagem enviada é um comando especificado pela plataforma. 

### broadcast(message, client)

- Função responsável por enviar uma mensagem a todos os clientes conectados, a exceção do cliente que enviou a própria mensagem


### handle(client)

- Essa função é executada em uma thread separada para cada cliente
- Responsável por lidar com a recepção de mensagens do cliente e execução das ações apropriadas com base nas mensagens recebidas

### receive()

- Aceita novas conexões de clientes, inicia um novo thread para lidar com cada cliente e realiza verificações e configurações iniciais.

### Inicialização

- O servidor começa a ouvir as conexões e chama a função receive