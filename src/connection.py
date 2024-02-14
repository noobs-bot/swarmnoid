import socket
import time
import cv2
from imutils.video import VideoStream
import matplotlib.pyplot as plt
import cv2.aruco as aruco
import numpy as np  # Add this line
from Identify_marker import identify_aruco_marker
from identify_palyground import detect_playground
from constants import *
from a_star_algo import *
from move_direction import calculate_commands

# Set the IP address and port on which the laptop server will listen
host = '0.0.0.0'  # Listen on all available interfaces
port = 2000  # Change if not working.

OrganicWate1 = True
OrganicWate2 = True
OrganicWate3 = True
OrganicWate4 = True
OrganicWate5 = True

Inorganicwate1 = True
Inorganicwate2 = True
Inorganicwate3 = True
Inorganicwate4 = True
Inorganicwate5 = True


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


def capture_video_pick(bot_id, waste_id):
    print(waste_id, bot_id)
    print("capture_video_pick")
    vc = cv2.VideoCapture(ip)
    _, frame = vc.read()
    roi_frame, playground = detect_playground(frame)
    if roi_frame is not None and playground is not None and roi_frame.any() and playground.any():
        # cv2.imshow("roi_frame ", roi_frame)
        # cv2.imshow("playground", playground)
        matrix, orientation, positions = identify_aruco_marker(playground)

        pick_path, matrix = position_Bot(bot_id, waste_id, matrix)
        if (pick_path is not None):
            print(f' pick_path = ', pick_path[bot_id])
            return pick_path[bot_id]
    return None

    # home_path, matrix = take_home(bot2, orgainic_waste[0], matrix)
    # # print(f'orientation = ', orientation)
    # print(f'home path = ', waste_path)


def capture_video_home(bot_id, waste_id):
    print(waste_id, bot_id)

    vc = cv2.VideoCapture(ip)
    _, frame = vc.read()
    roi_frame, playground = detect_playground(frame)
    if roi_frame is not None and playground is not None and roi_frame.any() and playground.any():
        # cv2.imshow("roi_frame ", roi_frame)
        # cv2.imshow("playground", playground)
        matrix, orientation, positions = identify_aruco_marker(roi_frame)
        home_path, matrix = take_home(bot_id, waste_id, matrix)

        if (home_path is not None):
            print(f' home path = ', home_path[bot_id])
            return home_path[bot_id]
    return None

    # home_path, matrix = take_home(bot2, orgainic_waste[0], matrix)
    # # print(f'orientation = ', orientation)
    # print(f'home path = ', waste_path)


# Create and establish a connection
server_socket, client_socket = establish_connection(host, port)


try:
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                raise Exception("Client disconnected")
            print("data = ", data.decode())
            while True:
                if (data.decode() == "Hello Server!"):
                    if (Inorganicwate1):
                        print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot1, inorganic_waste[0])
                        # print("pick path = ", pick_path)
                        if (pick_path is not None):
                            commands = calculate_commands(pick_path, bot1)
                            commands.append(bot1+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot1, inorganic_waste_home)
                        if (home_path is not None):
                            print("home path = ", home_path)

                            commands = calculate_commands(home_path, bot1)
                            commands.append(bot1+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        Inorganicwate1 = False


                        print("organic waste 1 = ", OrganicWate1)
                        # print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot2, orgainic_waste[0])
                        if (pick_path is not None):
                            print("pick path = ", pick_path)
                            commands = calculate_commands(pick_path, bot2)
                            commands.append(bot2+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot2, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot2)
                            commands.append(bot2+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        OrganicWate1 = False
                        print("organic waste 1 = ", OrganicWate1)

                    if (Inorganicwate2):
                        print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot1, inorganic_waste[1])
                        # print("pick path = ", pick_path)
                        if (pick_path is not None):
                            commands = calculate_commands(pick_path, bot1)
                            commands.append(bot1+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot1, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot1)
                            commands.append(bot1+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        Inorganicwate2 = False


                        print("organic waste 1 = ", OrganicWate1)
                        # print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot2, orgainic_waste[1])
                        if (pick_path is not None):
                            print("pick path = ", pick_path)
                            commands = calculate_commands(pick_path, bot2)
                            commands.append(bot2+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot2, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot2)
                            commands.append(bot2+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        OrganicWate2 = False
                        print("organic waste 1 = ", OrganicWate1)

                    if (Inorganicwate3):
                        print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot1, inorganic_waste[2])
                        # print("pick path = ", pick_path)
                        if (pick_path is not None):
                            commands = calculate_commands(pick_path, bot1)
                            commands.append(bot1+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot1, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot1)
                            commands.append(bot1+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        Inorganicwate3 = False


                        print("organic waste 1 = ", OrganicWate1)
                        # print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot2, orgainic_waste[2])
                        if (pick_path is not None):
                            print("pick path = ", pick_path)
                            commands = calculate_commands(pick_path, bot2)
                            commands.append(bot2+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot2, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot2)
                            commands.append(bot2+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        OrganicWate3 = False
                        print("organic waste 1 = ", OrganicWate1)

                        print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot1, inorganic_waste[3])
                        # print("pick path = ", pick_path)
                        if (pick_path is not None):
                            commands = calculate_commands(pick_path, bot1)
                            commands.append(bot1+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot1, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot1)
                            commands.append(bot1+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        Inorganicwate4 = False

                        print("organic waste 1 = ", OrganicWate1)
                        # print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot2, orgainic_waste[3])
                        if (pick_path is not None):
                            print("pick path = ", pick_path)
                            commands = calculate_commands(pick_path, bot2)
                            commands.append(bot2+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot2, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot2)
                            commands.append(bot2+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        OrganicWate4 = False
                        print("organic waste 1 = ", OrganicWate1)
                        print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot1, inorganic_waste[4])
                        # print("pick path = ", pick_path)
                        if (pick_path is not None):
                            commands = calculate_commands(pick_path, bot1)
                            commands.append(bot1+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot1, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot1)
                            commands.append(bot1+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        Inorganicwate5 = False

                        print("organic waste 1 = ", OrganicWate1)
                        # print("if condition = ", data.decode())
                        pick_path = capture_video_pick(
                            bot2, orgainic_waste[4])
                        if (pick_path is not None):
                            print("pick path = ", pick_path)
                            commands = calculate_commands(pick_path, bot2)
                            commands.append(bot2+"G")
                            print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                print("command = ", command)

                        time.sleep(2)

                        # print("if condition = ", data.decode())
                        home_path = capture_video_home(
                            bot2, inorganic_waste_home)
                        # print("pick path = ", pick_path)
                        if (home_path is not None):
                            commands = calculate_commands(home_path, bot2)
                            commands.append(bot2+"H")
                            # print("commands = ", commands)
                            for command in commands:
                                response = command
                                client_socket.sendall(response.encode())
                                time.sleep(1)  # Introduce a delay if needed
                                # print("command = ", command)
                        OrganicWate5 = False
                        print("organic waste 1 = ", OrganicWate1)
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

    # # # Get user input for commands
    # user_input = input(
    #     "Enter command (F/B/L/R/S to move, Q to quit): ").upper()

    # if user_input == 'Q':
    #     break
