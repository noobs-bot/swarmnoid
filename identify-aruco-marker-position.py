import cv2
import numpy as np

def calculate_orientation(marker_corners):
    # Calculate the orientation angle of the marker
    top_left = marker_corners[0]
    bottom_right = marker_corners[2]
    marker_orientation = np.arctan2(bottom_right[1] - top_left[1], bottom_right[0] - top_left[0])
    marker_orientation_deg = np.degrees(marker_orientation) % 360  # Ensure angle is between 0 and 360 degrees
    return marker_orientation_deg

def identify_aruco_marker_position(frame):
    grid_spacing = 50
    orientation = []
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
                    orientation.append((marker_id, calculate_orientation(corners_array)))
                    positions.append((marker_id, centroid, calculate_orientation(corners_array)))

                    # Draw a blue point at the centroid
                    cv2.circle(frame, tuple(centroid), 5, (255, 0, 0), -1)

        list_matrix = grid_matrix.tolist()

    return list_matrix, orientation, positions

if __name__=="__main__":
    # Open the video capture device
    vc = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video capture
        _, frame = vc.read()

        # Identify Aruco marker positions in the frame
        matrix, orientation, positions = identify_aruco_marker_position(frame)

        # Print positions and draw marker IDs on the frame
        print(f'position = ', positions)
        if orientation != []:
            diff = 0
            for item in orientation:
                print(item)
                cv2.putText(frame, f"ID: {item}", (50,50 + diff), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                diff = diff + 20

        # Display the frame
        cv2.imshow('Frame',frame)

        # Check for user input to exit the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # Release the video capture and close all windows
    vc.release()
    cv2.destroyAllWindows()
