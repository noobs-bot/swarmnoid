import cv2

video = cv2.VideoCapture(0)

while True:
    _,frame = video.read()
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
video.release()
cv2.destroyAllWindows()