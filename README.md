# chat-tcp
A python implementation of a 4-person chat using tcp

## Server.py

### list_to_string(list)

- Transforms a python list into a string, so we can send the elements via socket.

### is_command(message, command, size=0)

- Verifies if the message is a specified command on the platform.
- Size seria para uma implementação futura.

### broadcast(message, client)

- Sends the message to all clients connected, except for the sender.

### handle(client)

- Allows the connection of various clients, by creating a thread for each one of them.
- Handles the reception of messages and treats them accordingly, all the ifs are referent to the platform commands and error treatments.

### receive()

- Accept new client connections, making the initial security checks, initiating a new handle thread for each client.

## Client.py

### is_command(message, command, size=0)

- Same command as in the server.

### receive()

- Listens the server messages and makes the correct treatment.

### write()

- Keeps asking for keyboard inputs and lets the user comunicate with the server.
- Treats the delivery of the commands, avoiding miscomunication.
