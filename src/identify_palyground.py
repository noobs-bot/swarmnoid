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
ip_address = "http://192.168.1.153:4747/video"

# Initialize the VideoStream
# vs = VideoStream(src=ip_address).start()

# Allow the camera sensor to warm up
# (Note: For USB cameras, this step is not necessary)
cv2.waitKey(2000)

with open('camera.json', 'r') as json_file:
    camera_data = json.load(json_file)
dist = np.array(camera_data["dist"])
mtx = np.array(camera_data["mtx"])

def wrap_correction(frame, ids, corners):
    bottom_right = None
    bottom_left = None
    top_right = None
    top_left = None

    # cv2.imshow('original frame', frame)
    playground = None

    # Filter out markers that you want to use for perspective transformation
    valid_marker_ids = [0, 1, 2, 3]  # Update with the IDs of the markers you want to use
    valid_corners = [corner[0][1] for marker_id, corner in zip(ids, corners) if marker_id[0] in valid_marker_ids]

    if len(valid_corners) >= 4:
        # Sort corners based on marker positions
        sorted_corners = sorted(valid_corners, key=lambda x: x[0])

        # Extract corners in order
        top_left = tuple(map(int, sorted_corners[0]))
        top_right = tuple(map(int, sorted_corners[1]))
        bottom_left = tuple(map(int, sorted_corners[2]))
        bottom_right = tuple(map(int, sorted_corners[3]))

        # Check if all markers are detected before proceeding
        if None not in [bottom_right, bottom_left, top_right, top_left]:
            # Define the source and destination quadrilateral (frame)
            x1, y1 = top_left
            x2, y2 = top_right
            x3, y3 = bottom_left
            x4, y4 = bottom_right

            # Draw lines connecting the corners on the original frame
            frame = cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
            frame = cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
            frame = cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
            frame = cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)

            # Define the source and destination quadrilateral (frame)
            src_pts = np.array(
                [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], dtype=np.float32)

            # Define the destination rectangle (output size)
            width = int(max(np.linalg.norm(np.array([x2 - x1, y2 - y1])),
                            np.linalg.norm(np.array([x4 - x3, y4 - y3]))))
            height = int(max(np.linalg.norm(np.array([x3 - x1, y3 - y1])),
                             np.linalg.norm(np.array([x4 - x2, y4 - y2]))))

            dest_pts = np.array([(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)],
                                dtype=np.float32)

            # Compute the perspective transformation matrix
            matrix = cv2.getPerspectiveTransform(src_pts, dest_pts)

            # Apply the perspective transformation to the frame
            playground = cv2.warpPerspective(frame, matrix, (width, height))

            # Save the warped frame
            cv2.imwrite("images/playground.png", playground)

            # Display the warped frame
            cv2.imshow("playground", playground)

    return frame, playground


def main():
    print("[INFO] starting video stream...")
    # vs = VideoStream("http://192.168.1.153:4747/video").start()
    # vs = VideoStream(src=0).start()

    vs = cv2.VideoCapture(ip_address)
    _, frame = vs.read()

    while True:
        _, frame = vs.read()

        # time.sleep(2.0)
        cv2.imshow("original", frame)
        
        corners, ids, _ = aruco.detectMarkers(frame, aruco_dict)
        # print("Corner = ", corners)
        # print("IDS:  ",ids)
        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            frame, playground = wrap_correction(frame, ids, corners)

            cv2.imshow('ROI', frame)

            if playground is not None:
                cv2.imshow('Playground', playground)
                
        key = cv2.waitKey(1) & 0xFF
        
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    # do a bit of cleanup

    

    plt.show()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
