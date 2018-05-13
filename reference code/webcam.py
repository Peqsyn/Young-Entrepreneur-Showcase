import numpy
import cv2

cap = cv2.VideoCapture(0)
file = "C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\resources\\"
image_counter = 0

while(True):
	# capture frame by frame
	ret, image = cap.read()

	# display frame
	cv2.imshow('video output', image)

	keyPress = cv2.waitKey(10)& 0xFF
	if keyPress == 27: # this is the ASCII key for ESC button
		break
	if keyPress == 32: #this is the ASCII key for the space bar
		print("Space Bar Presesd")
		image_name = "image{}.jpeg".format(image_counter)
		cv2.imwrite(file + image_name, image)
		print("{} written!".format(image_name))
		image_counter += 1

# when everything done, release the capture
cap.release()
cv2.destroyAllWindows()