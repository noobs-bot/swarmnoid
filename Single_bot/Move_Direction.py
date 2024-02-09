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
                movement_commands.extend(["F"] * (x_distance // 200))  # Add forward commands
                time.sleep(2 * (x_distance // 200))  # Sleep to simulate movement time

        # Turn right or left
        if y_distance > 0:
            user_input = input(f"Turn {y_distance} units right? (Y/N): ")
            if user_input.upper() == "Y":
                movement_commands.extend(["R"] * (y_distance // 200))  # Add right turn commands
                time.sleep(4 * (y_distance // 200))  # Sleep to simulate turn time
        elif y_distance < 0:
            user_input = input(f"Turn {-y_distance} units left? (Y/N): ")
            if user_input.upper() == "Y":
                movement_commands.extend(["L"] * (-y_distance // 200))  # Add left turn commands
                time.sleep(4 * (-y_distance // 200))  # Sleep to simulate turn time

        # Update the current position
        current_position = (x, y)

    # Stop the robotic car
    movement_commands.append("S")  # Add stop command

    return movement_commands
