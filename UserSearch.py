import cv2
import dlib
import math
import face_recognition
from numpy import *


def UserSearch(face):
    #取眼部最下点 唇部最边上点的中点，做一下处理，得到一步rgb
    #对数据库中进行搜索
    #三十以下 就不管年龄，直接用rgb来搜索，变成一个o（N）的静态表的查找
