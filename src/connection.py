import socket
import time

# Set the IP address and port on which the laptop server will listen
host = '0.0.0.0'  # Listen on all available interfaces
port = 5000  # Change if not working.

OrganicWate1 = False
OrganicWate2 = False
OrganicWate3 = False
OrganicWate4 = False
OrganicWate5 = False


Inorganicwate1 = False
Inorganicwate2 = False
Inorganicwate3 = False
Inorganicwate4 = False
Inorganicwate5 = False


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
        try:
            data = client_socket.recv(1024)
            if not data:
                raise Exception("Client disconnected")
            while True:

                if (data.decode() == "Hello Server!"):
                    print("if condition = ", data.decode())

                    # Get user input for commands
                    user_input = input(
                        "Enter command (F/B/L/R/S to move, Q to quit): ").upper()

                    if user_input == 'Q':
                        break

                    # Send the user input to the client
                    client_socket.sendall(user_input.encode())
                    time.sleep(5)  # Adjust the sleep duration if needed
                    received_data = data.decode()
                    print(f"Received from client: {received_data}")
                    user_input = 'S'
                    client_socket.sendall(user_input.encode())
                    # time.sleep(1)

        except Exception as e:
            print(f"Exception occurred: {e}")
            # Close the client socket
            client_socket.close()

            # Wait and accept a new connection
            print("Waiting for a new connection...")
            server_socket.listen(1)
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    # Close the connection
    client_socket.close()
    server_socket.close()
    print("Socket connection closed.")
