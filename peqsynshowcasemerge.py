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

# folder location of temp
file = "C:\Users\ericl\Documents\Peqsyn\youngentrepreneurs\\temp\\"

# input in VideoCapture(0) for onboard webcam VideoCapture(1) for external camera
cap = cv2.VideoCapture(0)

# starts google vision annotator
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

# takes in a path, and analyzes the pictures using labels and web
def detect(path):
    image = start_detect(path)
    # grab labelAnnotations first
    response_label = client.label_detection(image=image)
    labels = response_label.label_annotations

    # grab webEntities second
    response_web = client.web_detection(image=image)
    webs = response_web.web_detection.web_entities

    # find matches top from labelAnnotations and webDetection
    # evaluate the scores from the matches
    (top_labels, top_labelDescriptions) = generate_label_list(labels)
    # puts labels in 2D array
    combined_Labels = [top_labels, top_labelDescriptions]
    print(combined_Labels)

    (top_webs, top_webDescriptions) = generate_web_list(webs)
    # puts webs in 2D array
    combined_Webs = [top_webs, top_webDescriptions]
    print(combined_Webs)
    # can reduce the top few lines into the generate function, just return 2D array
    
    # deciding on what the picture is    
    result = choice_algorithm(combined_Labels, combined_Webs)
    print(result[1])

def start_detect(path):
    # initializes detection
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    return image 

def generate_label_list(labels):
    # lists for labels
    possible_labels = []
    label_description = []
    top_labels = []
    top_descriptions = []

    # puts the score and descroption of the items into their own list 
    # so that we can do operations
    for i in range(len(labels)):
        possible_labels.append(labels[i].score)
        label_description.append(labels[i].description)
        # google orders the scores from highest to lowest automatically
        # take the top 3 highest scores and store into top_labels
        if (i < 3):
            top_labels.append(labels[i].score)
            top_descriptions.append(labels[i].description)
    return (top_labels, top_descriptions)

def generate_web_list(webs):
    # lists for webs
    possible_entity = []
    entity_description = []
    top_webs = []
    top_webDescriptions = []
    normalized_scores = []
    # puts the score and descroption of the items into their own list 
    # so that we can do operations
    for i in range(len(webs)):
        possible_entity.append(webs[i].score)
        entity_description.append(webs[i].description)
    # normalize data google does not normalize the data for webEntities
    web_max = max(possible_entity)
    web_min = min(possible_entity)
    for j in range(len(possible_entity)):
        normalized_scores.append((possible_entity[j] - web_min)/(web_max - web_min))

    # grab the top 3 results from the normalized scores
    for k in range(3):
        top_webs.append(normalized_scores[k])
        top_webDescriptions.append(webs[k].description)
    return (top_webs, top_webDescriptions)

def choice_algorithm(combined_Labels, combined_Webs):
    combined_Scores = []
    combined_Description = []
    combined_Result = []
    # only taking top 3, change accordingly if top result changes
    for i in range(3):
        combined_Scores.append(combined_Labels[0][i] + combined_Webs[0][i])
        combined_Description.append(combined_Labels[1][i] + " or " + combined_Webs[1][i])
    print (combined_Scores, combined_Description)
    combined_Result = (combined_Scores[0], combined_Description[0])
    return combined_Result

# runs webcam
def run_webcam():
    image_counter = 0
    while(True):
        # capture frame by frame
        ret, image = cap.read()

        # display frame
        if image is not None:
            cv2.imshow('video output', image)

        # checks for user input
        keyPress = cv2.waitKey(10)& 0xFF
        if keyPress == 27: # this is the ASCII key for ESC button
            stop_webcam()
        if keyPress == 32: #this is the ASCII key for the space bar
            take_picture(image_counter, image)
            call_googlevision()

def take_picture(image_counter, image):
    print("Picture Taken")
    # changing the range will determine the number of pictures taken by the camera with one click
    for i in range(1):
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
        #delay between taking pictures in seconds
        sleep(1)
        i = i + 1

def call_googlevision():
    path = load_temp()
    # detect_labels(path[image_counter])
    for i in range(len(path)):
        detect(path[i])
    # to analyze all files in the path
    # for i in range(len(path)):
        # detect_labels(path[i])
        # detect_web(path[i])

def stop_webcam():
    # when everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()

if __name__ == '__main__':
    run_webcam()