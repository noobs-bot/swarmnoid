# This is to test how different id aurco look like 
# Also for future when printing might be necessary

import cv2
import numpy as np

def aruco_marker_generator(marker_id, marker_size):

    # Define marker size and dictionary
    # It allows for a maximum of 250 markers. The 6x6 refers to the size of the individual markers in terms of bits.
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

    # Generate aruco marker
    marker_image = cv2.aruco.drawMarker(aruco_dict, marker_id, marker_size)
    # Assign the marker to the corresponding section in the image
    marker_image = cv2.cvtColor(marker_image, cv2.COLOR_GRAY2BGR)
    return marker_image

if __name__== "__main__" :
    marker_size = 200
    # Aruco marker size of 200 pixel

    # Create an image to draw the ArUco markers
    image_size = 800
    image = np.ones((image_size, image_size, 3), dtype=np.uint8) * 255
    # 3 represents three color channel BGR
    # Setting all pixel values to 255 results in white color

    positions = {
        0: (100, 100),
        1: (image_size - 100, 100),
        2: (image_size - 100, image_size - 100),
        3: (100, image_size - 100),
        4: (200, 200),
        5: (600, 600),
        6: (300, 300),
        7: (400, 400),
        8: (500, 300),
        9: (300, 500),
        10: (600, 200),
        11: (200, 600),
        # marker_id: position includes (x,y) coordinates
    }

    for marker_id, position in positions.items():
        marker_iamge = aruco_marker_generator(marker_id, marker_size)
        cv2.imwrite("images/Aurco/Aurco_{}.png".format(str(marker_id)), marker_iamge)
        cv2.imshow(str(marker_id), marker_iamge)

    # Display the generated ArUco markers
    cv2.waitKey(0)
    cv2.destroyAllWindows()
