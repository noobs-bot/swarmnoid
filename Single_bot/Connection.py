import socket
import time
from Move_Direction import calculate_commands
from A_star import assign_coordinates

def establish_connection(host, port):
    # Set the IP address and port on which the laptop server will listen
    # Listen on all available interfaces
    # Change port if needed.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    return server_socket, client_socket


# Given coordinates
coordinates = assign_coordinates()

# Set the IP address and port on which the laptop server will listen
host = '0.0.0.0'  # Listen on all available interfaces
port = 5000  # Change if not working.

# Create and establish a connection
server_socket, client_socket = establish_connection(host, port)

while True:
    # Receive a response from the client
    data = client_socket.recv(1024)
    if not data:
        break

    received_data = data.decode()
    print(f"Received from client: {received_data}")

    # Check if the trigger message is received
    if received_data.strip() == "Hello Server!":
        # Calculate commands and send them to the client
        movement_commands = calculate_commands(coordinates)
        for command in movement_commands:
            client_socket.sendall(command.encode())  # Send the encoded command
            time.sleep(2)  # Adjust the sleep duration if needed

# Close the connection
client_socket.close()
server_socket.close()
