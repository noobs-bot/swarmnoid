import cv2
from imutils.video import VideoStream
import matplotlib.pyplot as plt
import time
import cv2.aruco as aruco
import numpy as np
import imutils
import json 
from Grid import generate_matrix_from_image

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

with open('camera.json', 'r') as json_file:
	camera_data = json.load(json_file)
dist = np.array(camera_data["dist"])
mtx = np.array(camera_data["mtx"])


while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=1000)
	undistorted_frame = cv2.undistort(frame, mtx, dist)

	max_height = 600  
	if frame.shape[0] > max_height or undistorted_frame.shape[0] > max_height:
		aspect_ratio_frame = max_height / frame.shape[0]
		aspect_ratio_undistorted = max_height / undistorted_frame.shape[0]

		frame = cv2.resize(frame, (int(frame.shape[1] * aspect_ratio_frame), max_height))
		undistorted_frame = cv2.resize(
			undistorted_frame, (int(undistorted_frame.shape[1] * aspect_ratio_undistorted), max_height)
		)
	matrixA = generate_matrix_from_image(frame)
	matrixB = generate_matrix_from_image(undistorted_frame)
	print("matrixA",matrixA)
	print("matrixB",matrixB)
	frame = cv2.flip(frame, 1) 
	undistorted_frame = cv2.flip(undistorted_frame, 1) 
	cv2.imshow("Before", frame)
	cv2.imshow("After", undistorted_frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

plt.show()
cv2.destroyAllWindows()
vs.stop()
			
