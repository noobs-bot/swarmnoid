import time
import socket
from Move_Direction import command_bot
from a_star_test import main

def handle_bot(client_socket, bot_id, pick_path, return_path):
    bot_done = False
    bot_home = True

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        print(f"Received from bot {bot_id}: {data.decode()}")

        if bot_home and not bot_done:
            commands = command_bot(pick_path)
            for command in commands:
                if command.startswith(f"{bot_id}a") and not bot_done:
                    print(command)
                    response = command
                    client_socket.sendall(response.encode())
                    time.sleep(1)  # Introduce a delay if needed
            bot_done = True
            bot_home = False

        if not bot_home and bot_done:
            commands = command_bot(return_path)
            for command in commands:
                if command.startswith(f"{bot_id}a") and not bot_home:
                    print(command)
                    response = command
                    client_socket.sendall(response.encode())
                    time.sleep(1)  # Introduce a delay if needed
            bot_done = True
            bot_home = True

    # Close the connection when the loop breaks
    client_socket.close()

def main():
    host = "0.0.0.0"
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    
    bot1_pick_path = {1: [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)]}
    bot1_return_path = {1: [(3, 8), (3, 7), (3, 6), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1)]}

    while True:
        print(f"Connection from {client_address1}")
        handle_bot( bot1_pick_path, bot1_return_path)

if __name__ == "__main__":
    main()
