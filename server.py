import socket
import threading

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('0.0.0.0', 12946)  # Use 0.0.0.0 to listen on all available network interfaces

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening for connections...")

# List to store client connections
clients = []

# Function to broadcast messages to all connected clients
def broadcast(message, client_socket):
    for client in clients:
        # Send the message to all clients except the sender
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the client if unable to send the message
                clients.remove(client)

# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client
            message = client_socket.recv(1024)
            if not message:
                break
            # Broadcast the received message to all clients
            broadcast(message, client_socket)
        except:
            # Remove the client if there's an error
            clients.remove(client_socket)
            break

# Function to send a message to all connected clients
def send_to_clients(message):
    message = message.encode('utf-8')
    for client in clients:
        try:
            client.send(message)
        except:
            # Remove the client if unable to send the message
            clients.remove(client)

# Function for handling server-initiated messages
def server_message_handler():
    while True:
        message = input("-> Server message: ")
        send_to_clients(message)

# Create a thread for handling server-initiated messages
message_thread = threading.Thread(target=server_message_handler)
message_thread.start()
# Accept and handle incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    # Add the client to the list
    clients.append(client_socket)
    
    # Create a thread to handle the client's messages
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    
    # Send a welcome message to the newly connected client
    welcome_message = f"Welcome {client_address}!"
    send_to_clients(welcome_message)
