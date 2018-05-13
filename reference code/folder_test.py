import cv2
import os

def load_image():
	images = []
	for filename in os.listdir('resources'):
		# if not filename.endswith('.png', '.jpg', '.jpeg', '.gif', '.bmp'):
		# 	continue
		filepath = os.path.join('resourcs', filename)
		print(filepath)
		images.append(filepath)
	# print(filepath)
	# print(type(filepath))
	# print(type(images))
	# print(images)

load_image()