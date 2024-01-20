import cv2
import numpy as np
from ArucoGeneration import aruco_marker_generator

# Create an image to place ArUco markers
aurco_size = 50 # also equals grid size in px
no_of_grid = 22 # number of grids | 22 rows & 22 columns
image_size = aurco_size * no_of_grid # horizintal length = vertical length = 50*22 = 1100 px

canvas = np.ones((image_size, image_size, 3), dtype=np.uint8) * 255
# canvas size of 1100*1100 px



# Positions for markers 0-3 from top-left to bottom-right corners and waste collection 4 & 5
positions = {
    0: (aurco_size, aurco_size), #topleft
    1: (aurco_size, image_size - aurco_size*2),#topright
    2: (image_size - aurco_size*2, aurco_size), #bottomleft
    3: (image_size - aurco_size*2, image_size - aurco_size*2), #bottomright
    4: (11*aurco_size,aurco_size), #nororganic waste center
    5: (aurco_size, 11*aurco_size) #organic waste center
}

# Generate markers with IDs 0-5 and place them on the canvas
for marker_id, position in positions.items():
    # Aruco marker generation
    marker =  aruco_marker_generator(marker_id, marker_size=50)
    x, y = position
    canvas[y:y + 50, x:x + 50] = marker

# definings markder Ids, and position
positions_bot_waste_y = {
    6: [(14*aurco_size, 9*aurco_size)], #bot 1
    7: [(11*aurco_size, 11*aurco_size)], #bot 2
    8: [ #8 is non organic
        (7*aurco_size,7*aurco_size),
        (7*aurco_size,14*aurco_size),
        (14*aurco_size,15*aurco_size),
        (11*aurco_size,18*aurco_size),
        (18*aurco_size,7*aurco_size)
        ],
    9: [ #9 is organic
        (8*aurco_size,9*aurco_size),
        (12*aurco_size,9*aurco_size),
        (9*aurco_size,13*aurco_size),
        (8*aurco_size,18*aurco_size),
        (18*aurco_size,13*aurco_size)
        ],
}

# Generate markers with IDs 6 - 9 and place them in playable grid
for marker_id, positions_list in positions_bot_waste_y.items():
    for position in positions_list:
        marker = aruco_marker_generator(marker_id ,marker_size=50)
        x, y = position
        canvas[y:y + aurco_size, x:x + aurco_size] = marker


# Defining Playabe gird
# Define the start and end points of the line as tuples
point1 = (100, 100)
point2 = (image_size-100, 100)
point3 = (100, image_size-100)
point4 = (image_size-100, image_size-100)

# Define the color of the line (BGR format)
color = (0, 0, 255)  # Red in BGR

# Specify the thickness of the line
thickness = 2

# Draw the line on the image
cv2.line(canvas, point1, point2, color, thickness)
cv2.line(canvas, point1, point3, color, thickness)
cv2.line(canvas, point2, point4, color, thickness)
cv2.line(canvas, point3, point4, color, thickness)

# defining new playabe canvas
playabe_canvas =  np.ones((image_size, image_size, 3), dtype=np.uint8) * 255


# Display the image with ArUco markers
cv2.imshow("ArUco Markers", canvas)
cv2.imwrite("images/TestGround.png", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
