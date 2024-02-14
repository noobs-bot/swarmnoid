import time


def calculate_commands(coordinates, bot):
    movement_commands = []  # Initialize the list of movement commands
    # Initialize the current position of the robot
    current_position = coordinates[0]

    # Loop through each set of coordinates starting from the second one
    for coord in coordinates[1:]:
        x, y = coord

        # Calculate the differences in x and y coordinates
        dx = x - current_position[0]
        dy = y - current_position[1]

        # Generate movement commands based on the differences
        if dx > 0:
            movement_commands.append(bot + "F")  # Move forward
        elif dx < 0:
            movement_commands.append(bot + "B")  # Move backward

        if dy > 0:
            movement_commands.append(bot + "R")  # Turn right
        elif dy < 0:
            movement_commands.append(bot + "L")  # Turn left

        # Update the current position
        current_position = coord

    movement_commands.append(bot + "S")  # Stop the robotic car
    return movement_commands


if __name__ == "__main__":
    coordinates = [(2, 20), (2, 19), (2, 18), (2, 17), (2, 16), (2, 15), (2, 14), (2, 13), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12),
                   (12, 12), (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12), (19, 12), (20, 12), (21, 12), (22, 12), (23, 12), (24, 12), (25, 12), (26, 12), (27, 12), (28, 12), (28, 11)]
    print(calculate_commands(coordinates, "6"))
