import socket
import time

# Set the IP address and port on which the laptop server will listen
host = '0.0.0.0'  # Listen on all available interfaces
port = 5000  # Change if not working.

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

# Create and establish a connection
server_socket, client_socket = establish_connection(host, port)

try:
    while True:
        # Get user input for commands
        user_input = input("Enter command (F/B/L/R/S to move, Q to quit): ").upper()

        if user_input == 'Q':
            break

        # Send the user input to the NodeMCU
        client_socket.sendall(user_input.encode())
        time.sleep(1)  # Adjust the sleep duration if needed
        user_input = 'S'
        client_socket.sendall(user_input.encode())
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    # Close the connection
    client_socket.close()
    server_socket.close()
    print("Socket connection closed.")
