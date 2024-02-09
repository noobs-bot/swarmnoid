import cv2
from imutils.video import VideoStream
import matplotlib.pyplot as plt
import cv2.aruco as aruco
import numpy as np  # Add this line
from Identify_marker import identify_aruco_marker
from identify_palyground import detect_playground
from constants import *
from a_star_algo import *

if __name__ == "__main__":
    print("[INFO] starting video stream...")
    vc = cv2.VideoCapture(1)
    while True:
        _, frame = vc.read()
        roi_frame, playground = detect_playground(frame)
        if roi_frame is not None and playground is not None and roi_frame.any() and playground.any():
            cv2.imshow("roi_frame ", roi_frame)
            cv2.imshow("playground", playground)
            matrix, orientation, positions = identify_aruco_marker(playground)

            # for bot1 : 6 id -> organic bot
            # bot1
            # inorganic_waste
            waste_path, matrix = position_Bot(bot1, inorganic_waste[0], matrix)
            # print(f'orientation = ', orientation)
            print(f'waste path = ', waste_path)

            home_path, matrix = take_home(bot2, orgainic_waste[0], matrix)
            # print(f'orientation = ', orientation)
            print(f'home path = ', waste_path)

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    # frame = cv2.imread("images/original.png")
    # roi_frame, playground = detect_playground(frame)
    # if roi_frame is not None and playground is not None and roi_frame.any() and playground.any():
    #     cv2.imshow("roi_frame ", roi_frame)
    #     cv2.imshow("playground", playground)
    #     matrix, orientation, positions = identify_aruco_marker(playground)
    #     print(f'orientation = ', orientation)

    # key = cv2.waitKey(0)
    plt.show()
    cv2.destroyAllWindows()
