import time
from Move_Direction import command_bot
import socket

# Set the IP address and port on which the laptop server will listen
host = '0.0.0.0'  # Listen on all available interfaces
port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(2)
print(f"Server listening on {host}:{port}")

# Accept a connection
client_socket1, client_address1 = server_socket.accept()
print(f"Connection from {client_address1}")
print(f"Server listening on {host}:{port}")

# Accept a connection
client_socket2, client_address2 = server_socket.accept()
print(f"Connection from {client_address2}")
bot1_done = False
bot2_done = False
while True:
    # Receive a response from the client
    data1 = client_socket1.recv(1024)
    if not data1:
        break
    data2 = client_socket2.recv(1024)
    if not data2:
        break
    print(f"Received from client: {data1.decode()}")
    # print(f"Received from client: {data2.decode()}")

    # Send a response back to the client
    # str(dir) + ":" + str(time)
    test_data = [{1: [(9, 14), (9, 13), (10, 13), (10, 12)]}, {2: [(11, 11), (11, 10), (11, 9), (11, 8), (12, 8), (13, 8), (14, 8), (15, 8), (15, 7)]}]
    commands = command_bot(test_data)
    for command in commands:
        if command[0]=='1' and bot1_done == False:
            print(command)
            response = command
            client_socket1.sendall(response.encode())
            # time.sleep(1)
        if command[0]=='2' and bot2_done == False:
            print(command)
            response = command
            client_socket2.sendall(response.encode())
        time.sleep(1)
    bot1_done = True
    bot2_done = True
# Close the connection
client_socket1.close()
client_socket2.close()
server_socket.close()