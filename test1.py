from ImageSearch import *
import cv2
import dlib
import cv2
import math 
img=cv2.imread('4.jpeg')
detector = dlib.get_frontal_face_detector()
print imageSearch(img)
