#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations with the
Google Cloud Vision API.

Example Usage:
python detect.py labels ./resources/wakeupcat.jpg
python detect.py labels ./resources/landmark.jpg
python detect.py labels ./resources/landmark.jpg
python detect.py web-uri http://wheresgus.com/dog.JPG
python detect.py faces-uri gs://your-bucket/file.jpg

For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import io

import os
import cv2
import numpy

from google.cloud import vision
from google.cloud.vision import types

# path = 'C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\resources'
cap = cv2.VideoCapture(0)
# change to resources if want to upload a bunch of pictures
# file = "C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\resources\\"
file = "C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\temp\\"

# [START def load_res]
def load_res():
	images_res = []
	for filename in os.listdir('resources'):
		# if not filename.endswith('.png', '.jpg', '.jpeg', '.gif', '.bmp'):
		# 	continue
		filepath = os.path.join('resources', filename)
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

	# for filename in os.listdir('temp'):
	# 	filepath = os.path.join('temp', filename)
	# 	os.remove(file + filename)
	# 	print("Deleted files")
	# 	break
	for filename in os.listdir('temp'):
		filepath = os.path.join('temp', filename)
		images_temp.append(filepath)
		print("Added files")
	# print(filepath)
	# print(type(filepath))
	# print(images)
	return images_temp
# [END def load_temp]

# [START def GUI]
# def GUI(str):
# 	#create the window
# 	root = Tk()

# 	topFrame = Frame(root)
# 	topFrame.pack()



# 	#modify root window
# 	root.title("Food Scanner")
# 	root.geometry("500x250")

# 	app = Frame(root)
# 	app.grid()
# 	# label = Label(app, text = "Capture")

# 	button1 = Button(app, text = "This is a button")
# 	button1.grid()

# 	button2 = Button(app)
# 	button2.grid()
# 	button2.configure(text = "This will show text")

# 	button3 = Button(app)
# 	button3.grid()

# 	button3["text"] = "This will show up as well"

# 	# label.grid()

# 	#keep window open
# 	root.mainloop()
# [END def GUI]

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
    location = possible_labels.index(max(possible_labels))
    
    # displays result of what item was scanned
    print("A(n) " + label_description[location] + ' was placed into the system')

    # this is used to figure out what the api sees
    # for label in labels:
    # 	print(len(labels))
        #print(label.description)
        #print(label.score)

    # [END migration_label_detection]
# [END def_detect_labels]


# [START def_detect_labels_uri]
# def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    # client = vision.ImageAnnotatorClient()
    # image = types.Image()
    # image.source.image_uri = uri

    # response = client.label_detection(image=image)
    # labels = response.label_annotations
    # print('Labels:')

    # for label in labels:
    #     print(label.description)
# [END def_detect_labels_uri]


# [START def_detect_web]
# def detect_web(path):
    """Detects web annotations given an image."""
    # client = vision.ImageAnnotatorClient()

    # [START migration_web_detection]
    # with io.open(path, 'rb') as image_file:
    #     content = image_file.read()

    # image = types.Image(content=content)

    # response = client.web_detection(image=image)
    # notes = response.web_detection

    # if notes.pages_with_matching_images:
    #     print('\n{} Pages with matching images retrieved')

    #     for page in notes.pages_with_matching_images:
    #         print('Url   : {}'.format(page.url))

    # if notes.full_matching_images:
    #     print ('\n{} Full Matches found: '.format(
    #            len(notes.full_matching_images)))

    #     for image in notes.full_matching_images:
    #         print('Url  : {}'.format(image.url))

    # if notes.partial_matching_images:
    #     print ('\n{} Partial Matches found: '.format(
    #            len(notes.partial_matching_images)))

    #     for image in notes.partial_matching_images:
    #         print('Url  : {}'.format(image.url))

    # if notes.web_entities:
    #     print ('\n{} Web entities found: '.format(len(notes.web_entities)))

    #     for entity in notes.web_entities:
    #         print('Score      : {}'.format(entity.score))
    #         print('Description: {}'.format(entity.description))
    # [END migration_web_detection]
# [END def_detect_web]


# [START def_detect_web_uri]
# def detect_web_uri(uri):
#     """Detects web annotations in the file located in Google Cloud Storage."""
#     client = vision.ImageAnnotatorClient()
#     image = types.Image()
#     image.source.image_uri = uri

#     response = client.web_detection(image=image)
#     notes = response.web_detection

#     if notes.pages_with_matching_images:
#         print('\n{} Pages with matching images retrieved')

#         for page in notes.pages_with_matching_images:
#             print('Url   : {}'.format(page.url))

#     if notes.full_matching_images:
#         print ('\n{} Full Matches found: '.format(
#                len(notes.full_matching_images)))

#         for image in notes.full_matching_images:
#             print('Url  : {}'.format(image.url))

#     if notes.partial_matching_images:
#         print ('\n{} Partial Matches found: '.format(
#                len(notes.partial_matching_images)))

#         for image in notes.partial_matching_images:
#             print('Url  : {}'.format(image.url))

#     if notes.web_entities:
#         print ('\n{} Web entities found: '.format(len(notes.web_entities)))

#         for entity in notes.web_entities:
#             print('Score      : {}'.format(entity.score))
#             print('Description: {}'.format(entity.description))
# [END def_detect_web_uri]

# [START def run_webcam
def run_webcam():
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
			# print("Space Bar Presesd")
			# image_name = "image{}.jpeg".format(image_counter)
			image_name = "image.jpeg"
			if (os.path.exists(file + image_name)):
				os.remove(file + image_name)
			cv2.imwrite(file + image_name, image)
			# print("{} written!".format(image_name))
			# image_counter += 1

			# get path to sub into detect_labels
			path = load_temp()
			for i in range(len(path)):
			    detect_labels(path[i])
# [END def run_webcam]

# [START def stop_webcam]
def stop_webcam():
	# when everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
# [END def stop_webcam]

# def run_local(args):
#     if args.command == 'labels':
#         detect_labels(args.path)
#     elif args.command == 'web':
#     	detect_web(args.path)

# def run_uri(args):
#     if args.command == 'labels-uri':
#         detect_labels_uri(args.uri)
#     elif args.command == 'web-uri':
#     	detect_web_uri(args.path)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter)
    # subparsers = parser.add_subparsers(dest='command')

    # detect_labels_parser = subparsers.add_parser(
    #     'labels', help=detect_labels.__doc__)
    # detect_labels_parser.add_argument('path')

    # labels_file_parser = subparsers.add_parser(
    #     'labels-uri', help=detect_labels_uri.__doc__)
    # labels_file_parser.add_argument('uri')

    # #not implemented yet
    # web_parser = subparsers.add_parser(
    #     'web', help=detect_web.__doc__)
    # web_parser.add_argument('path')

    # web_uri_parser = subparsers.add_parser(
    #     'web-uri',
    #     help=detect_web_uri.__doc__)
    # web_uri_parser.add_argument('uri')

    # args = parser.parse_args()

    # if ('uri' in args.command):
    #     run_uri(args)
    # else:
    #    	run_local(args)
	run_webcam()