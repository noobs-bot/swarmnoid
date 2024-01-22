import cv2
import cv2.aruco as aruco
import numpy as np

def extract_playground(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define the ArUco dictionary and parameters
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    arucoParams = cv2.aruco.DetectorParameters_create()

    # Detect markers in the image
    corners, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters=arucoParams)

    # Check if markers were detected
    if ids is not None and len(ids) >= 4:
        # Draw the detected markers on the image
        image_with_markers = aruco.drawDetectedMarkers(image.copy(), corners, ids)
        cv2.imshow("image with markers", image_with_markers)

        # Extract the corners of the markers
        top_left_corner = corners[ids.tolist().index(0)][0][0]
        top_right_corner = corners[ids.tolist().index(1)][0][1]
        bottom_left_corner = corners[ids.tolist().index(2)][0][3]
        bottom_right_corner = corners[ids.tolist().index(3)][0][2]

        # Define the region of interest (ROI) using the extracted corners
        roi_corners = np.array([top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner], dtype=np.int32)
        roi_corners = roi_corners.reshape((-1, 1, 2))

        # Create a mask to extract the area
        mask = np.zeros_like(gray)
        cv2.fillPoly(mask, [roi_corners], 255)

        # Extract the area connecting the four edges
        result = cv2.bitwise_and(image, image, mask=mask)
        return result

    else:
        # If markers are not detected, return the original image
        return image

if __name__ == "__main__":
    vc = cv2.VideoCapture(0)
    while True:
        _, frame = vc.read()
        playground = extract_playground(frame)
        cv2.imshow("Playground", playground)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

cv2.destroyAllWindows()
vc.release()
