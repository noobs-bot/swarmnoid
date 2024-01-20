import time
from Move_Direction import command_bot
from a_star_test import main

import socket

# Set the IP address and port on which the laptop server will listen
host = '0.0.0.0'  # Listen on all available interfaces
port = 1111

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


bot1_done = False
bot1_home = True
bot2_done = False
bot2_home = True
while True:
    # Receive a response from the client
    data1 = client_socket1.recv(1024)
    if not data1:
        break
 
    print(f"Received from client: {data1.decode()}")
    # print(f"Received from client: {data2.decode()}")

    # Send a response back to the client
    # str(dir) + ":" + str(time)

    # pick_path, return_path = main()

    pick_path = {1: [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)]}

    if  bot1_home and not bot1_done:
        commands = command_bot(pick_path)
        for command in commands:
         if command[0]=='1' and bot1_done == False:
            print(command)
            response = command
            client_socket1.sendall(response.encode())
            # time.sleep(1)
    bot1_done = True
    bot1_home = False



    if not bot1_home and bot1_done:
        
        path = pick_path # You need to define pick_path based on your logic
        commands = command_bot(path)
    
        for command in commands:
         if command[0] == '1':
            print(command)
            response = command
            client_socket1.sendall(response.encode())
            # time.sleep(1)  # Optionally, introduce a delay if needed
    bot1_home = True
   





# Close the connection
client_socket1.close()
server_socket.close()