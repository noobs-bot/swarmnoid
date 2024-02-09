import cv2
from imutils.video import VideoStream
import matplotlib.pyplot as plt
import time
import cv2.aruco as aruco
import numpy as np  # Add this line
import imutils
import json


# Define the ArUco dictionary and parameters
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
markersX = 2  # Number of markers in the X direction
markersY = 2  # Number of markers in the Y direction
markerLength = 0.02  # Length of each marker
markerSeparation = 0.04  # Separation between markers
firstMarker = 0  # ID of the first marker (default is 0)

# Create the grid board with four markers in the four corners
board = aruco.GridBoard_create(
    markersX, markersY, markerLength, markerSeparation, aruco_dict, firstMarker)
# board.setMarkerIds(marker_ids)
# board.setMarkerCorners(marker_positions)

# Replace the IP address with the correct address of your camera stream
# ip_address = "http://192.168.1.153:4747/video"

# cv2.waitKey(2000)

with open('camera.json', 'r') as json_file:
    camera_data = json.load(json_file)
dist = np.array(camera_data["dist"])
mtx = np.array(camera_data["mtx"])


def wrap_correction(frame, marker_data):
    playground = None

    # Extract the marker IDs and corner points from the marker_data list
    marker_ids = [marker_id[0] for marker_id, _ in marker_data]
    corners = [corner_points for _, corner_points in marker_data]

    # Define the required marker IDs
    required_marker_ids = [0, 1, 3, 2]

    if not all(marker_id in marker_ids for marker_id in required_marker_ids):
        # If any required marker ID is missing, return None for both frame and playground
        return None, None

    # Filter out markers that you want to use for perspective transformation
    valid_marker_data = [(marker_id, corner) for marker_id, corner in zip(marker_ids, corners) if marker_id in required_marker_ids]

    if len(valid_marker_data) == 4:
        # Sort marker data based on marker IDs
        sorted_marker_data = sorted(valid_marker_data, key=lambda x: x[0])

        # Extract sorted corners
        sorted_corners = [corner for _, corner in sorted_marker_data]

        # Extract corners in order
        # Extract the first corner of each marker
        top_left = tuple(map(int, sorted_corners[0][0][0]))
        bottom_left = tuple(map(int, sorted_corners[1][0][0]))
        bottom_right = tuple(map(int, sorted_corners[3][0][0]))
        top_right = tuple(map(int, sorted_corners[2][0][0]))

        # Define the source and destination quadrilateral (frame)
        x1, y1 = top_left  # 0 marker
        x2, y2 = bottom_left  # 1 marker
        x3, y3 = bottom_right  # 3 marker
        x4, y4 = top_right  # 2 marker

        # Draw lines connecting the corners on the original frame
        frame = cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
        frame = cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
        frame = cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
        frame = cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)

        # Define the source and destination quadrilateral (frame)
        src_pts = np.array(
            [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.float32)
        # top left, bottom left, bottom right, top right

        # Define the destination rectangle (output size)
        width = int(max(np.linalg.norm(np.array([x4 - x1, y4 - y1])),
                        np.linalg.norm(np.array([x3 - x2, y3 - y2]))))
        height = int(max(np.linalg.norm(np.array([x2 - x1, y2 - y1])),
                         np.linalg.norm(np.array([x3 - x4, y3 - y4]))))

        dest_pts = np.array([(0, 0), (0, height - 1), (width - 1, height - 1), (width - 1, 0)],
                            dtype=np.float32)

        # Compute the perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(src_pts, dest_pts)

        # Apply the perspective transformation to the frame
        playground = cv2.warpPerspective(frame, matrix, (width, height))

        # Save the warped frame
        cv2.imwrite("images/playground.png", playground)

    return frame, playground


def detect_playground(frame):
    playground = None
    roi_frame = None
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # time.sleep(2.0)
    # cv2.imshow("original", frame)
    corners, ids, _ = aruco.detectMarkers(frame, aruco_dict)
    # Combine respective IDs and corners into a list of tuples
    marker_data = [(marker_id, corner_points)
                   for marker_id, corner_points in zip(ids, corners)]

# Print the list of tuples
    # print("marker_data = ", marker_data)
    # print("Corner = ", corners)
    # print("IDS:  ", ids)
    if ids is not None:

        # aruco.drawDetectedMarkers(frame, corners, ids)
        # cv2.imshow("original", frame)
        roi_frame, playground = wrap_correction(frame, marker_data)
        # if playground is not None:
        #     cv2.imshow('Playground', playground)
    return roi_frame, playground


if __name__ == "__main__":
    print("[INFO] starting video stream...")
    # vs = cv2.VideoCapture("http://192.168.1.153:4747/video")
    vs = cv2.VideoCapture(1)

    # # Get the current resolution
    # current_width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
    # current_height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # # Calculate the new resolution (double the width and height)
    # new_width = current_width * 2
    # new_height = current_height * 2

    # # Set the new resolution
    # vs.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
    # vs.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

    while True:
        _, frame = vs.read()
        # cv2.imwrite("images/original.png", frame)

        cv2.imshow("original", frame)

        roi_frame, playground = detect_playground(frame)
        if roi_frame is not None and playground is not None and roi_frame.any() and playground.any():
            cv2.imshow("roi_frame ", roi_frame)
            cv2.imshow("playground", playground)

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    # do a bit of cleanup
    plt.show()
    cv2.destroyAllWindows()
