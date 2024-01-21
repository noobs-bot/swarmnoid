import numpy as np


def handle_rotation(current_orientation, new_rotation):
    output = []

    if current_orientation != new_rotation:
        if current_orientation == "F":
            if new_rotation == "R":
                output.append("R")
            elif new_rotation == "L":
                output.append("L")
            elif new_rotation == "B":
                output.append("L")
                output.append("L")
        elif current_orientation == "R":
            if new_rotation == "L":
                output.append("L")
                output.append("L")
            elif new_rotation == "F":
                output.append("L")
            elif new_rotation == "B":
                output.append("R")
        elif current_orientation == "B":
            if new_rotation == "L":
                output.append("R")
            elif new_rotation == "F":
                output.append("L")
                output.append("L")
            elif new_rotation == "R":
                output.append("L")
        elif current_orientation == "L":
            if new_rotation == "R":
                output.append("L")
                output.append("L")
            elif new_rotation == "F":
                output.append("R")
            elif new_rotation == "B":
                output.append("L")

    return new_rotation, output


def move_direction(nodes):
    current_node = None
    output = []
    orientation = "F"

    for node in nodes:
        next_node = node
        if current_node is None:
            current_node = next_node
        elif next_node[1] < current_node[1]:
            orientation, data = handle_rotation(orientation, "R")
            output.extend(data)
            output.append("F")  
        elif next_node[1] > current_node[1]:
            orientation, data = handle_rotation(orientation, "L")
            output.extend(data)
            output.append("F") 
        elif next_node[0] < current_node[0]:
            orientation, data = handle_rotation(orientation, "B")
            output.extend(data)
            output.append("B")  
        elif next_node[0] > current_node[0]:
            orientation, data = handle_rotation(orientation, "F")
            output.extend(data)
            output.append("F")

        current_node = next_node

    return output


def get_bot1_value(data):
    if 1 in data and isinstance(data[1], list):
        return data[1]
    elif 1 in data and isinstance(data[1], int):
        return [data[1]]
    else:
        return []


def command_bot(data):
    bot1 = get_bot1_value(data)

    bot1_movement = move_direction(bot1)
    print(bot1_movement)
    response_list = []

    for movement in bot1_movement:
        response_list.append(f"1a{movement}b10")

    return response_list
