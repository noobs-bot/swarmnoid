import cv2
import numpy as np

def calculate_orientation(marker_corners):
    top_left = marker_corners[0]
    bottom_right = marker_corners[2]

    # Calculating orientation angle
    marker_orientation = np.arctan2(bottom_right[1] - top_left[1], bottom_right[0] - top_left[0])
    marker_orientation_deg = np.degrees(marker_orientation) % 360  # Ensure angle is between 0 and 360 degrees
    return marker_orientation_deg

def generate_matrix_from_image(frame):
    grid_spacing = 50
    orientation =[]
    list_matrix = []

    if frame is None:
        print("Error: Image not found or unable to load.")
        exit(0)

    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    arucoParams = cv2.aruco.DetectorParameters_create()

    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    if ids is not None:
        matrix_size = frame.shape[0] // grid_spacing, frame.shape[1] // grid_spacing
        grid_matrix = np.empty(matrix_size, dtype=object)
        grid_matrix.fill('a')

        for i, marker_id in enumerate(ids.flatten()):
            corners_array = corners[i][0]
            if len(corners_array) > 0:
                centroid = np.mean(corners_array, axis=0, dtype=np.int32)
                cell_x = centroid[0] // grid_spacing
                cell_y = centroid[1] // grid_spacing

                if cell_x < matrix_size[1] and cell_y < matrix_size[0]:
                    grid_matrix[cell_y, cell_x] = marker_id
                    orientation.append((marker_id,calculate_orientation(corners_array)))
        list_matrix = grid_matrix.tolist()
    return list_matrix,orientation

vc = cv2.VideoCapture(0)
while True:
    _,frame = vc.read()
    matrix, orientation = generate_matrix_from_image(frame)
    if orientation != []:
        print(orientation)
        cv2.putText(frame, f"ID: {orientation[0]}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    cv2.imshow('Frame',frame)
    key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
cv2.destroyAllWindows()