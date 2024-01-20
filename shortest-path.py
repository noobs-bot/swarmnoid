import cv2
import numpy as np
from queue import PriorityQueue

def calculate_orientation(marker_corners):
    top_left = marker_corners[0]
    bottom_right = marker_corners[2]
    marker_orientation = np.arctan2(bottom_right[1] - top_left[1], bottom_right[0] - top_left[0])
    marker_orientation_deg = np.degrees(marker_orientation) % 360
    return marker_orientation_deg

def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def astar(matrix, start, end, obstacles):
    print("executing a star")
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def is_valid(x, y):
        print(f'lenght = {len(matrix)}')
        print('x = ', x)
        print('y = ', y)
        valid = 0 <= x < len(matrix) and 0 <= y < len(matrix) and matrix[y][x] == 'a'
        if not valid:
            print(f"Invalid position: x={x}, y={y}")
        return valid

    start = (start[1], start[0])  # Swap x and y for A* algorithm
    end = (end[1], end[0])

    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while not open_set.empty():
        current = open_set.get()[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Return reversed path

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            print("before validation")
            if not is_valid(neighbor[0], neighbor[1]) or neighbor in obstacles:
                continue
            print("after validation")
            tentative_g_score = g_score[current] + heuristic(current, neighbor)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                open_set.put((f_score[neighbor], neighbor))

    return None  # No path found

def identify_aruco_marker_position(frame):
    grid_spacing = 50
    positions = []
    list_matrix = []

    if frame is None:
        print("Error: Image not found or unable to load.")
        exit(0)

    # Aruco marker detection parameters
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    arucoParams = cv2.aruco.DetectorParameters_create()

    # Detect Aruco markers in the frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

    if ids is not None:
        # Create a grid matrix to store marker IDs
        matrix_size = frame.shape[0] // grid_spacing, frame.shape[1] // grid_spacing
        grid_matrix = np.empty(matrix_size, dtype=object)
        grid_matrix.fill('a')

        for i, marker_id in enumerate(ids.flatten()):
            corners_array = corners[i][0]

            if len(corners_array) > 0:
                # Draw a polygon around the detected marker
                corner_tuples = np.array(corners_array, dtype=np.int32)
                cv2.polylines(frame, [np.array(corner_tuples)], True, (0, 255, 0), 2)

                # Calculate centroid of the marker and its grid cell position
                centroid = np.mean(corners_array, axis=0, dtype=np.int32)
                cell_x = centroid[0] // grid_spacing
                cell_y = centroid[1] // grid_spacing

                # Update grid matrix with marker ID at the corresponding cell
                if cell_x < matrix_size[1] and cell_y < matrix_size[0]:
                    grid_matrix[cell_y, cell_x] = marker_id
                    # orientation.append((marker_id, calculate_orientation(corners_array)))
                    positions.append((marker_id, centroid, calculate_orientation(corners_array)))

                    # Draw a blue point at the centroid
                    cv2.circle(frame, tuple(centroid), 5, (255, 0, 0), -1)

        list_matrix = grid_matrix.tolist()

    return list_matrix, positions

if __name__=="__main__":
    vc = cv2.VideoCapture(0)

    while True: 
        _, frame = vc.read()
        matrix, orientation, positions = identify_aruco_marker_position(frame)

        # print(f'matrix = {matrix}')
        # print(f'positions = {positions}')


        if positions != []:
            diff = 15
            for item in positions:
                print(item)
                cv2.putText(frame, f"ID: {item}, ", (50,50 + diff), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                diff = diff + 20

        # Find marker positions for IDs 1 and 2
        marker_1_position = None
        marker_2_position = None
        for marker_id, position, _ in positions:
            if marker_id == 1:
                marker_1_position = position
            elif marker_id == 2:
                marker_2_position = position

        if marker_1_position is not None and marker_2_position is not None:
            # print("condition meet")
            # Find path using A* algorithm
            obstacles = set([tuple(pos) for _, pos, _ in positions if not np.all(pos == marker_1_position) and not np.all(pos == marker_2_position)])
            path = astar(matrix, marker_1_position, marker_2_position, obstacles)
            # Draw the path on the frame
            print('f path = ', path)
            if path:
                for point in path:
                    cv2.circle(frame, (point[1], point[0]), 1, (0, 255, 255), -1)

                # Draw lines connecting consecutive points in the path
                for i in range(len(path) - 1):
                    cv2.line(frame, (path[i][1], path[i][0]), (path[i+1][1], path[i+1][0]), (0, 255, 255), 1)

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    vc.release()
    cv2.destroyAllWindows()
