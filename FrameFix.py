import cv2
from imutils.video import VideoStream
import matplotlib.pyplot as plt
import time
import cv2.aruco as aruco
import numpy as np
import imutils
import json 




# Define the ArUco dictionary and parameters
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
markersX = 2  # Number of markers in the X direction
markersY = 2  # Number of markers in the Y direction
markerLength = 0.02  # Length of each marker
markerSeparation = 0.04 # Separation between markers
firstMarker = 0  # ID of the first marker (default is 0)

# Create the grid board with four markers in the four corners
board = aruco.GridBoard_create(markersX, markersY, markerLength, markerSeparation, aruco_dict, firstMarker)
# board.setMarkerIds(marker_ids)
# board.setMarkerCorners(marker_positions)

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

with open('camera.json', 'r') as json_file:
	camera_data = json.load(json_file)
dist = np.array(camera_data["dist"])
mtx = np.array(camera_data["mtx"])

def wrap_correction():
	if len(ids) >= 4:
		#corners detected in order (true_id -> corner_id )0 -> 3, 1 -> 2, 2 -> 1, 3 -> 0,
		for id in ids:
			id_marker = int(id[0])
			if id_marker == 0:
				bottom_right = tuple(map(int, corners[3][0][2]))
			elif id_marker == 1:
				bottom_left = tuple(map(int, corners[2][0][3]))
			elif id_marker == 2:
				top_right = tuple(map(int, corners[1][0][1]))
			elif id_marker == 3:
				top_left = tuple(map(int,corners[0][0][0]))


		four_corners = [bottom_right,bottom_left,top_right,top_left]
		# Define the source and destination quadrilateral (frame)
		x1,y1 = top_left
		x2,y2 = top_right
		x3, y3 = bottom_left
		x4, y4 = bottom_right
	
		# Define the source and destination quadrilateral (frame)
		src_pts = np.array([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], dtype=np.float32)

		# Define the destination rectangle (output size)
		width = int(max(np.linalg.norm(np.array([x2-x1, y2-y1])), np.linalg.norm(np.array([x4-x3, y4-y3]))))
		height = int(max(np.linalg.norm(np.array([x3-x1, y3-y1])), np.linalg.norm(np.array([x4-x2, y4-y2]))))

		dest_pts = np.array([(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)], dtype=np.float32)

		# Compute the perspective transformation matrix
		matrix = cv2.getPerspectiveTransform(src_pts, dest_pts)

		# Apply the perspective transformation to the frame
		warped = cv2.warpPerspective(frame, matrix, (width, height))

		#apply occupancy grid in the code below
		#cv2.imshow("Cropped",warped)
		img = warped
		print("Frame shape---->", img.shape)
		assert img is not None, "file could not be read, check with os.path.exists()"
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
					cv2.THRESH_BINARY,11,2)
		th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
					cv2.THRESH_BINARY,11,2)
		count = 0
		numbers = []
		rows = len(thresh[0])
		for val in thresh:
			for i in val:
				numbers.append(i) if i not in numbers else None
				if i == 255:
					count+=1
		print("Total numberes in a row---",rows)
		print("Total objects--", count)
		print("Total available numbers----", numbers)
		print("Threshold Size -- and type ----", thresh.shape, type(thresh))

		import numpy as np

		# Assuming 'matrix' is your 1100x1500 matrix
		# For illustration purposes, let's create a sample matrix
		matrix = th3

		# Define the size of the squares
		square_size = 15 # You can adjust this based on your preference 1100/50

		# Calculate the number of squares in each dimension
		num_rows = matrix.shape[0] // square_size
		num_cols = matrix.shape[1] // square_size

		# Create an empty grid to store probabilities
		probability_grid = np.zeros((num_rows, num_cols))

		# Iterate through each square in the matrix
		for i in range(num_rows):
			for j in range(num_cols):
				# Extract the current square from the matrix
				square = matrix[i * square_size: (i + 1) * square_size, j * square_size: (j + 1) * square_size]

				# Calculate the probability of an object in the square
				object_count = np.count_nonzero(square == 255)
				total_elements = square.size
				probability = object_count / total_elements

				# Store the probability in the grid
				probability_grid[i, j] = probability

	return frame

while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 1000 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=1000)
	corners, ids, _ = aruco.detectMarkers(frame, aruco_dict)
	#print("Corner", corners)
	#print("IDS:  ",ids)
	if ids is not None:
		aruco.drawDetectedMarkers(frame, corners, ids)
		retval, rvec, tvec = aruco.estimatePoseBoard(corners, ids, board, mtx, dist, rvec = None,tvec = None)
		R, _ = cv2.Rodrigues(rvec)

		# Extract angles from the rotation matrix (3x3 rotation matrix)
		theta_x = np.arctan2(R[2, 1], R[2, 2])
		theta_y = np.arctan2(-R[2, 0], np.sqrt(R[2, 1] ** 2 + R[2, 2] ** 2))
		theta_z = np.arctan2(R[1, 0], R[0, 0])
		# Calculate angles in radians
		theta_x_rad = np.arctan2(R[2, 1], R[2, 2])  # Pitch
		theta_y_rad = np.arctan2(-R[2, 0], np.sqrt(R[2, 1] ** 2 + R[2, 2] ** 2))
		theta_z_rad = np.arctan2(R[1, 0], R[0, 0])  # Yaw

		# Convert radians to degrees
		theta_x_deg = np.degrees(theta_x_rad)
		theta_y_deg = np.degrees(theta_y_rad)
		theta_z_deg = np.degrees(theta_z_rad)

		# Normalize angles to the range of 0-360 degrees
		theta_x_360 = theta_x_deg % 360
		theta_y_360 = theta_y_deg % 360
		theta_z_360 = theta_z_deg % 360

		print("pitch:", theta_x_360)
		print("yaw:",theta_z_360)
		print("roll:", theta_y_360)
		cv2.putText(frame, "pitch:{}".format(theta_x_360), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.putText(frame, "yaw:{}".format(theta_z_360), (50,150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.putText(frame, "roll:{}".format(theta_y_360), (50,250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		frame = wrap_correction()

			
			

			

	cv2.imshow("frame",frame)	

	
		#if retval:
		#	cv2.drawFrameAxes(frame, mtx, dist, rvec, tvec, 5)
			
	
	# Crop the frame
	

	#cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
# do a bit of cleanup
plt.show()
cv2.destroyAllWindows()
vs.stop()
			
#python detect_board.py --type DICT_6X6_250

