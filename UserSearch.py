import cv2
import dlib
import math
import face_recognition
from numpy import *


def UserSearch(face):
    #ȡ�۲����µ� ��������ϵ���е㣬��һ�´����õ�һ��rgb
    #�����ݿ��н�������
    #��ʮ���� �Ͳ������䣬ֱ����rgb�����������һ��o��N���ľ�̬��Ĳ���
