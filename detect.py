# Gomi SHIFT prototype

import argparse
import io

import os
import cv2
import numpy

from google.cloud import vision
from google.cloud.vision import types

# path = 'C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\resources'

# change to resources if want to upload a bunch of pictures
# file = "C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\resources\\"
file = "C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\temp\\"
# file = "C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\walmart_test\\"

# [START def load_res]
def load_res():
	images_res = []
	for filename in os.listdir('walmart_test'):
		# if not filename.endswith('.png', '.jpg', '.jpeg', '.gif', '.bmp'):
		# 	continue
		filepath = os.path.join('walmart_test', filename)
		# print(filepath)
		images_res.append(filepath)
	# print(filepath)
	# print(type(filepath))
	# print(images)
	return images_res
# [END def load_res]

# [START def load_temp]
def load_temp():
	images_temp = []
	for filename in os.listdir('temp'):
		filepath = os.path.join('temp', filename)
		images_temp.append(filepath)
		print("Added files")
	# print(filepath)
	# print(type(filepath))
	# print(images)
	return images_temp
# [END def load_temp]

# [START def_detect_labels]
def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    possible_labels = []
    label_description = []
    # puts the score and descroption of the items into their own list 
    # so that we can do operations
    for i in range(len(labels)):
    	possible_labels.append(labels[i].score)
    	label_description.append(labels[i].description)

    # finds the item with the highest score and the index in the list
    # location = possible_labels.index(max(possible_labels))
    
    # displays result of what item was scanned
    # print("A(n) " + label_description[location] + ' was placed into the system')

    # this is used to figure out what the api sees
    # for label in labels:
    # 	print(len(labels))
        #print(label.description)
        #print(label.score)
# [END def_detect_labels]

# [START def_detect_web]
def detect_web(path):
	# Run 1
    """Detects web annotations given an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_web_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.web_detection(image=image)
    notes = response.web_detection.web_entities

    possible_entity = []
    entity_description = []
    # puts the score and descroption of the items into their own list 
    # so that we can do operations
    for i in range(len(notes)):
    	possible_entity.append(notes[i].score)
    	entity_description.append(notes[i].description)

    # finds the item with the highest score and the index in the list
    location = possible_entity.index(max(possible_entity))
    print("Run 1: A(n) " + entity_description[location] + ' was placed into the system')

	# Run 2
    # [START migration_web_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.web_detection(image=image)
    notes = response.web_detection.web_entities

    possible_entity = []
    entity_description = []
    # puts the score and descroption of the items into their own list 
    # so that we can do operations
    for i in range(len(notes)):
    	possible_entity.append(notes[i].score)
    	entity_description.append(notes[i].description)

    # finds the item with the highest score and the index in the list
    compare = possible_entity.index(max(possible_entity))
    print("Run 2: A(n) " + entity_description[compare] + ' was placed into the system')
    count = 0;

    while (location != compare):
    	with io.open(path, 'rb') as image_file:
	    content = image_file.read()

	    image = types.Image(content=content)

	    response = client.web_detection(image=image)
	    notes = response.web_detection.web_entities

	    possible_labels = []
	    label_description = []
	    # puts the score and descroption of the items into their own list 
	    # so that we can do operations
	    for i in range(len(notes)):
	    	possible_labels.append(notes[i].score)
	    	label_description.append(notes[i].description)

	    # finds the item with the highest score and the index in the list
	    if count == 3:
	    	location = possible_labels.index(max(possible_labels))
	    	count = 0;
	    else:
	    	compare = possible_labels.index(max(possible_labels))
	    	count = count + 1
	    print('Run{}: This is iteration'.format(count))
    # displays result of what item was scanned
    print("A(n) " + entity_description[compare] + ' was placed into the system')
    # [END migration_web_detection]
# [END def_detect_web]

# [START def run_webcam
def run_webcam():
	# use 0 for onboard webcam, use 1 for external webcam
	cap = cv2.VideoCapture(0)
	image_counter = 0
	while(True):
		# capture frame by frame
		ret, image = cap.read()

		# display frame
		cv2.imshow('video output', image)

		keyPress = cv2.waitKey(10)& 0xFF
		if keyPress == 27: # this is the ASCII key for ESC button
			stop_webcam()
		if keyPress == 32: #this is the ASCII key for the space bar
			print("Space Bar Presesd")
			# image_name = "image{}.jpeg".format(image_counter)
			image_name = "image.jpeg"
			if (os.path.exists(file + image_name)):
				os.remove(file + image_name)
			cv2.imwrite(file + image_name, image)
			# print("{} written!".format(image_name))
			# image_counter += 1

			# get path to sub into detect_labels
			path = load_temp()
			# path = load_res()
			for i in range(len(path)):
			    # detect_labels(path[i])
			    detect_web(path[i])
# [END def run_webcam]

# [START def stop_webcam]
def stop_webcam():
	# when everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
# [END def stop_webcam]

if __name__ == '__main__':
	run_webcam()
	# path = load_res()
	# for i in range(len(path)):
		# detect_web(path[i])