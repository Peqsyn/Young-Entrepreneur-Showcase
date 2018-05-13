# Peqsyn showcase

import argparse
import io
import sys

import os
import cv2
import numpy

from google.cloud import vision
from google.cloud.vision import types
from time import sleep

# path = 'C:\Users\ericl\Documents\Gomi Technologies\oppfest\\vision_detect\\resources'

# change to resources if want to upload a bunch of pictures
file = "C:\Users\ericl\Documents\Peqsyn\youngentrepreneurs\\temp\\"

# input in VideoCapture(0) for onboard webcam VideoCapture(1) for external camera
cap = cv2.VideoCapture(0)
client = vision.ImageAnnotatorClient()

# loads images captured into temp directory and returns the path of the directory as a list
# should create new directory everytime there is a new run
def load_temp():
    images_temp = []
    for filename in os.listdir('temp'):
        # TODO: check to see if file already exists if it does then skip

        # TODO: create new directory if running again
        filepath = os.path.join('temp', filename)
        images_temp.append(filepath)
        # print("Added files")
        print images_temp
        print type(images_temp)
    return images_temp

# takes in a path, and analyzes the pictures using labels
def detect_labels(path):
    # """Detects labels in the file."""
    # client = vision.ImageAnnotatorClient()

    # # [START migration_label_detection]
    # with io.open(path, 'rb') as image_file:
    #     content = image_file.read()

    # image = types.Image(content=content)
    image = start_detect(path)

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

# takes in a path, and analyzes the pictures using web
def detect_web(path):
    # Run 1
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

# [START def run_webcam
def run_webcam():
    image_counter = 0
    while(True):
        # capture frame by frame
        ret, image = cap.read()

        # display frame
        if image is not None:
            cv2.imshow('video output', image)

        keyPress = cv2.waitKey(10)& 0xFF
        if keyPress == 27: # this is the ASCII key for ESC button
            stop_webcam()
        if keyPress == 32: #this is the ASCII key for the space bar
            print("Picture Taken")
            for i in range(10):
                image_name = "image{}.jpeg".format(image_counter)
                if (os.path.exists(file + image_name)):
                    os.remove(file + image_name)
                cv2.imwrite(file + image_name, image)
                image_counter = image_counter + 1
                # capture frame by frame
                ret, image = cap.read()
                # display frame
                if image is not None:
                    cv2.imshow('video output', image)
                sleep(0.5)
                i = i + 1
            # get path to sub into detect_labels
            path = load_temp()
            # detect_labels(path[image_counter])
            for i in range(len(path)):
                detect_labels(path[i])
            # to analyze all files in the path
            # for i in range(len(path)):
                # detect_labels(path[i])
                # detect_web(path[i])

def start_detect(path):
    # initializes detection
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    return image

def stop_webcam():
    # when everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()
# [END def stop_webcam]

if __name__ == '__main__':
    run_webcam()