import time


def calculate_commands(coordinates):
    movement_commands = []  # Use a different variable name to avoid conflicts
    current_position = (0, 0)  # Initialize the current position of the robot

    for coord in coordinates:  # Loop through each set of coordinates
        x, y = coord

        # Calculate the distance to move along the x-axis
        x_distance = x - current_position[0]

        # Calculate the distance to move along the y-axis
        y_distance = y - current_position[1]

        # Move forward
        if x_distance > 0:
            user_input = input(f"Move {x_distance} units forward? (Y/N): ")
            if user_input.upper() == "Y":
                # Add forward commands
                movement_commands.extend(["F"] * (x_distance // 200))
                # Sleep to simulate movement time
                time.sleep(2 * (x_distance // 200))

        # Turn right or left6y7v
        if y_distance > 0:
            user_input = input(f"Turn {y_distance} units right? (Y/N): ")
            if user_input.upper() == "Y":
                # Add right turn commands
                movement_commands.extend(["R"] * (y_distance // 200))
                # Sleep to simulate turn time
                time.sleep(4 * (y_distance // 200))
        elif y_distance < 0:
            user_input = input(f"Turn {-y_distance} units left? (Y/N): ")
            if user_input.upper() == "Y":
                # Add left turn commands
                movement_commands.extend(["L"] * (-y_distance // 200))
                # Sleep to simulate turn time
                time.sleep(4 * (-y_distance // 200))

        # Update the current position
        current_position = (x, y)

    # Stop the robotic car
    movement_commands.append("S")  # Add stop command

    return movement_commands


if __name__ == "__main__":
    coordinates = [(3, 1), (3, 2), (3, 3), (3, 4),
                   (3, 5), (3, 6), (3, 7), (3, 8)]
    print(calculate_commands(coordinates))
    # Call the function with the given coordinates
    movement_commands = calculate_commands(coordinates)
