import heapq
# from matrix import generate_matrix_from_image
import cv2
import numpy as np
from Identify_marker import identify_aruco_marker


def get_neighbors(node, matrix):
    """
    Get neighboring nodes of a given node in the matrix.

    Parameters:
    - node: Tuple representing the coordinates of the current node.
    - matrix: 2D matrix representing the environment.

    Returns:
    - List of neighboring nodes.
    """
    row, col = node
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    matrix_size = len(matrix)  # square shape matrix
    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy
        if (
            0 <= new_row < matrix_size
            and 0 <= new_col < matrix_size
            and (matrix[new_row][new_col] == "a" or matrix[new_row][new_col] == "b")
        ):
            neighbors.append((new_row, new_col))
    return neighbors


def astar(start, goal, matrix):
    """
    A* algorithm to find the shortest path between start and goal nodes in the matrix.

    Parameters:
    - start: Tuple representing the starting coordinates.
    - goal: Tuple representing the goal coordinates.
    - matrix: 2D matrix representing the environment.

    Returns:
    - List of coordinates representing the shortest path.
    """
    heap = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while heap:
        current_cost, current_node = heapq.heappop(heap)

        if current_node == goal:
            break

        for next_node in get_neighbors(current_node, matrix):
            new_cost = cost_so_far[current_node] + \
                1  # Assuming each step costs 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                heapq.heappush(heap, (priority, next_node))
                came_from[next_node] = current_node

    if goal in came_from:
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
    else:
        return None


def heuristic(node, target):
    """
    Heuristic function for the A* algorithm.

    Parameters:
    - node: Tuple representing the current node.
    - target: Tuple representing the target node.

    Returns:
    - Heuristic value.
    """
    return abs(node[0] - target[0]) + abs(node[1] - target[1])


def draw_matrix(matrix, path=[]):
    """
    Draw the matrix with optional path overlay.

    Parameters:
    - matrix: 2D matrix representing the environment.
    - path: List of coordinates representing the path to be overlayed.

    Returns:
    - Image of the matrix with optional path overlay.
    """
    matrix_size = len(matrix)  # Assuming matrix is a square matrix

    yellow = (0, 255, 255)
    green = (0, 255, 0)

    blue = (0, 0, 255)
    # offset_green = (122, 255, 122)
    # offset_red = (255, 122, 122)
    # red_blue = (255, 0, 255)  # bot for red inorganic bot
    # green_blue = (0, 255, 255)  # bot for green organic bot
    red = (255, 0, 0)
    gray = (125, 125, 125)
    pink = (203, 192, 255)
    orange = (0, 165, 255)
    black = (0, 0, 0)
    white = (255, 255, 255)

    cell_size = 20
    height, width = matrix_size * cell_size, matrix_size * cell_size
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

    for i in range(matrix_size):
        for j in range(matrix_size):
            color = white
            if matrix[i][j] == 4:
                color = yellow
            elif matrix[i][j] == 5:
                color = green
            elif matrix[i][j] == 6:
                color = red
            elif matrix[i][j] == 7:
                color = blue
            elif (
                matrix[i][j] == 8
                or matrix[i][j] == 10
                or matrix[i][j] == 12
                or matrix[i][j] == 14
                or matrix[i][j] == 16
            ):
                color = pink
            elif (
                matrix[i][j] == 9
                or matrix[i][j] == 11
                or matrix[i][j] == 13
                or matrix[i][j] == 15
                or matrix[i][j] == 17
            ):
                color = orange
            # elif (
            #     matrix[i][j] == 0
            #     or matrix[i][j] == 1
            #     or matrix[i][j] == 2
            #     or matrix[i][j] == 3
            #     or matrix[i][j] == 4
            #     or matrix[i][j] == 5
            # ):
            #     color = blue
            # elif 8 < i < 14 and (j == 2 or j == 3 or j == 4):
            #     color = green
            # elif 8 < j < 14 and (i == 2 or i == 3 or i == 4):
            #     color = red

            elif matrix[i][j] == "b":
                color = black

            cv2.rectangle(
                canvas,
                (j * cell_size, i * cell_size),
                ((j + 1) * cell_size, (i + 1) * cell_size),
                color,
                -1,
            )
    # Draws path
    if path:
        for node in path:
            cv2.rectangle(
                canvas,
                (node[1] * cell_size, node[0] * cell_size),
                ((node[1] + 1) * cell_size, (node[0] + 1) * cell_size),
                gray,
                -1,
            )
    # Draws matrixlines
    for i in range(0, width, cell_size):
        cv2.line(canvas, (i, 0), (i, height), black, 1)
    for j in range(0, height, cell_size):
        cv2.line(canvas, (0, j), (width, j), black, 1)

    return canvas


def find_closest_indices(matrix, bot_id, waste_id):
    """
    Find the closest start and end indices for a given bot and waste in the matrix.

    Parameters:
    - matrix: 2D matrix representing the environment.
    - bot_id: Identifier for the bot.
    - waste_id: Identifier for the waste.

    Returns:
    - Tuple containing closest start and end indices, and the minimum distance.
    """
    matrix_array = np.array(matrix)
    start_nodes = np.argwhere(matrix_array == bot_id)
    end_nodes = np.argwhere(matrix_array == waste_id)

    if len(start_nodes) > 0 and len(end_nodes) > 0:
        min_distance = float("inf")
        closest_start = None
        closest_end = None

        for s_node in start_nodes:
            for e_node in end_nodes:
                distance = abs(s_node[0] - e_node[0]) + \
                    abs(s_node[1] - e_node[1])
                if distance < min_distance:
                    min_distance = distance
                    closest_start = tuple(s_node)
                    closest_end = tuple(e_node)

        return closest_start, closest_end, min_distance

    return None


def position_Bot(
    bot_id, waste_id, matrix
):  # img_id is just for output of process and is not nedded
    """
    Move the bot to pick up waste and update the matrix.

    Parameters:
    - bot_id: Identifier for the bot.
    - waste_id: Identifier for the waste.
    - matrix: 2D matrix representing the environment.

    Returns:
    - Final path and updated matrix.
    """
    final_path = []
    matrix_array = np.array(matrix)

    closest_indices = find_closest_indices(
        matrix_array, str(bot_id), str(waste_id))
    if closest_indices is not None:
        closest_start, closest_end, min_distance = find_closest_indices(
            matrix_array, str(bot_id), str(waste_id)
        )

        closest_end = (closest_end[0] + 1, closest_end[1])
        path = astar(closest_start, closest_end, matrix)
        matrix[closest_end[0] - 1][closest_end[1]] = "b"
        matrix[closest_start[0]][closest_start[1]] = "a"
        matrix[closest_end[0]][closest_end[1]] = str(bot_id)
        matrix_array = np.array(matrix)

        final_path.append({bot_id: path})
        # print("closest indices found for bot {}. = ".format(bot_id), path)
        cv2.imwrite('images/Dijkstar/bot1/{}Pathmatrix.png'.format(bot_id),
                    draw_matrix(matrix, path))
        cv2.imshow('From Bot - {} to Waste - {}'.format(bot_id,
                   waste_id), draw_matrix(matrix, path))

    else:
        print("No closest indices found for bot {}.".format(bot_id))
        return None, None
    final_path = final_path[0] if final_path else {}
    return final_path, matrix


# img_id is just for output of process and is not nedded

# img_id is just for output of process and is not nedded
def take_home(bot_id, waste_id, matrix):
    """
    Move the bot to take waste home and update the matrix.

    Parameters:
    - bot_id: Identifier for the bot.
    - waste_id: Identifier for the waste.
    - matrix: 2D matrix representing the environment.

    Returns:
    - Final path and updated matrix.
    """
    final_path = []
    matrix_array = np.array(matrix)

    closest_indices = find_closest_indices(
        matrix_array, str(bot_id), str(waste_id))
    if closest_indices is not None:
        closest_start, closest_end, min_distance = find_closest_indices(
            matrix_array, str(bot_id), str(waste_id)
        )

        closest_end = (closest_end[0] + 1, closest_end[1] + 2)
        path = astar(closest_start, closest_end, matrix)
        matrix[closest_start[0]][closest_start[1]] = 'a'
        matrix[closest_start[0] - 1][closest_start[1]] = 'a'
        matrix[closest_end[0]][closest_end[1]] = str(bot_id)
        matrix_array = np.array(matrix)

        final_path.append({bot_id: path})

        cv2.imwrite('images/Dijkstar/bot1/{}Pushmatrix.png'.format(bot_id),
                    draw_matrix(matrix, path))
        cv2.imshow('Home Path - {}'.format(bot_id), draw_matrix(matrix, path))
    else:
        print("No closest indices found for bot {}.".format(bot_id))
        return None, None

    final_path = final_path[0] if final_path else {}
    return final_path, matrix


def main(frame):
    matrix, orientation, positions = identify_aruco_marker(frame)
    matrix_array = np.array(matrix)
    if positions != []:
        diff = 15
        for item in positions:
            # print(item)
            cv2.putText(
                frame,
                f"ID: {item}, ",
                (50, 50 + diff),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1,
            )
            diff = diff + 20

    # Find marker positions for IDs 1 and 2
    # marker_1_position = None
    # marker_2_position = None
    # for marker_id, position, _ in positions:
    #     if marker_id == 1:
    #         marker_1_position = position
    #     elif marker_id == 2:
    #         marker_2_position = position

        pick_path = []
        return_path = []
        # if find_closest_indices(matrix_array, '4', '5'):
        obj_path, matrix = position_Bot(bot, waste, matrix)
        ret_path, matrix = take_home(bot, home, matrix)
        pick_path.append(obj_path)
        return_path.append(ret_path)


if __name__ == "__main__":
    # vc = cv2.VideoCapture('http://192.168.1.153:4747/video')
    vc = cv2.VideoCapture(1)

    while True:
        _, frame = vc.read()
        # Identify Aruco marker positions in the frame
        main(frame)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
