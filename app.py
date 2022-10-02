from flask import Flask
app = Flask(__name__)

import cv2
import numpy as np
from PIL import Image
from flask import jsonify,request

Known_distance = 50.2
Known_width = 14.3


# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):

	# finding the focal length
	focal_length = (width_in_rf_image * measured_distance) / real_width
	return focal_length

# distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):

	distance = (real_face_width * Focal_Length)/face_width_in_frame

	# return the distance
	return distance

def face_data(image):

	face_width = 0 # making face width to zero

	# converting color image to gray scale image
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# detecting face in the image
	faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

	# looping through the faces detect in the image
	# getting coordinates x, y , width and height
	for (x, y, h, w) in faces:

		# getting face width in the pixels
		face_width = w

	# return the face width in pixel
	return face_width


def distance_from_screen():
	# reading reference_image from directory
	ref_image = cv2.imread("Ref_image.png")
	ref_image_face_width = face_data(ref_image)
	Focal_length_found = Focal_Length_Finder(
		Known_distance, Known_width, ref_image_face_width)
	img = Image.open(request.files['file'])
	frame = np.array(img)
	face_width_in_frame = face_data(frame)
	Distance = Distance_finder(
		Focal_length_found, Known_width, face_width_in_frame)

	return jsonify({'distance': round(Distance,2)})

@app.route('/', methods=['POST', 'GET'])
def get_distance():
	return distance_from_screen()

