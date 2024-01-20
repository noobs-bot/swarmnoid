import numpy as np

def handle_rotation(current_orientation, new_rotation):
    output = []

    if current_orientation != new_rotation:
        if current_orientation == 'F':
            if new_rotation == 'R':
                output.append('R')
            elif new_rotation == 'L':
                output.append('L')
            elif new_rotation == 'B':
                output.append('L')
                output.append('L')
        elif current_orientation == 'R':
            if new_rotation == 'L':
                output.append('L')
                output.append('L')
            elif new_rotation == 'F':
                output.append('L')
            elif new_rotation == 'B':
                output.append('R')
        elif current_orientation == 'B':
            if new_rotation == 'L':
                output.append('R')
            elif new_rotation == 'F':
                output.append('L')
                output.append('L')
            elif new_rotation == 'R':
                output.append('L')
        elif current_orientation == 'L':
            if new_rotation == 'R':
                output.append('L')
                output.append('L')
            elif new_rotation == 'F':
                output.append('R')
            elif new_rotation == 'B':
                output.append('L')

    return new_rotation, output

def move_direction(nodes):
    current_node = None
    output = []
    orientation = 'F'
    for node in nodes:
        next_node = node
        if current_node is None:
            current_node = next_node
        elif next_node[1] < current_node[1]:
            orientation,data = handle_rotation(orientation,'R')
            output.extend(data)
            output.extend('F')
        elif next_node[1] > current_node[1]:
            orientation,data = handle_rotation(orientation,'L')
            output.extend(data)
            output.extend('F')
        elif next_node[0] < current_node[0]:
            orientation,data = handle_rotation(orientation,'B')
            output.extend(data)
            output.extend('B')
        elif next_node[0] > current_node[0]:
            orientation,data = handle_rotation(orientation,'F')
            output.extend(data)
            output.extend('F')

        current_node = next_node

    return output

def command_bot(data):
    bot1 = next((d.get(1, []) for d in data if 1 in d), [])

    bot2 = next((d.get(2, []) for d in data if 2 in d), [])

    bot1_movement = move_direction(bot1)
    bot2_movement = move_direction(bot2)

    max_length = max(len(bot1_movement), len(bot2_movement))
    response_list = []
    
    for i in range(max_length):
        if i < len(bot1_movement) and i < len(bot2_movement):
            response_list.append(f"1a{bot1_movement[i]}b10")
            response_list.append(f"2a{bot2_movement[i]}b10")
        elif i < len(bot1_movement):
            response_list.append(f"1a{bot1_movement[i]}b10")
        elif i < len(bot2_movement):
            response_list.append(f"2a{bot2_movement[i]}b10")   

    return response_list  


