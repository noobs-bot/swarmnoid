def bot_handler(client_socket, address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {address} disconnected.")
                break

            print(f"Received from client {address}: {data.decode()}")

            # Simulate getting the path from the camera module or queue
            if not path_queue.empty():
                new_path = path_queue.get()
                commands = command_bot({"1": new_path})
            else:
                commands = command_bot({"1": [(2, 3), (2, 4), (2, 6), (2, 7)]})

            for command in commands:
                # Instead of sending to NodeMCU, print the command
                print(f"Sending to NodeMCU: {command}")

                # You can also simulate a delay here if needed
                time.sleep(1)

    finally:
        client_socket.close()
