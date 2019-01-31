import cv2
import face_recognition
import numpy as np

def s():
    img=cv2.imread("3_t.png")
    face_list=face_recognition.face_landmarks(img)
    p=[]
    for k in face_list[0]["right_eye"]:
        p.append([k[0],k[1]])
    pts=np.array(p,np.int32)
    pts=pts.reshape((-1,1,2))
    minn=-1
    right_eye_x=0
    right_eye_y=0
    for k in pts:
        if k[0][0]>minn:
            minn=k[0][0]
            right_eye_x=k[0][0]
            right_eye_y=k[0][1]
    p=[]
    for k in face_list[0]["left_eye"]:
        p.append([k[0],k[1]])
    pts=np.array(p,np.int32)
    pts=pts.reshape((-1,1,2))
    maxx=100000
    left_eye_x=0
    left_eye_y=0
    for k in pts:
        if k[0][0]<maxx:
            maxx=k[0][0]
            left_eye_x=k[0][0]
            left_eye_y=k[0][1]

    p=[]
    for k in face_list[0]["top_lip"]:
        p.append([k[0],k[1]])
    pts=np.array(p,np.int32)
    pts=pts.reshape((-1,1,2))
    minn=100000
    maxx=-1
    left_lip_x=0
    left_lip_y=0
    right_lip_x=0
    right_lip_y=0
    for k in pts:
        if k[0][0]<minn:
            minn=k[0][0]
            left_lip_x=k[0][0]
            left_lip_y=k[0][1]
        if k[0][0]>maxx:
            maxx=k[0][0]
            right_lip_x=k[0][0]
            right_lip_y=k[0][1]

    left_x=(left_lip_x+left_eye_x)/2
    left_y=(left_lip_y+left_eye_y)/2

    right_x=(right_lip_x+right_eye_x)/2
    right_y=(right_lip_y+right_eye_y)/2

    light1=int(img[right_y][right_x][0])+int(img[right_y][right_x][1])+int(img[right_y][right_x][2])
    light2=int(img[left_y][left_x][0])+int(img[left_y][left_x][1])+int(img[left_y][left_x][2])
    if light1>light2:
        #bgr->rbg
        return [img[right_y][right_x][2],img[right_y][right_x][0],img[right_y][right_x][1]]
    else:
        return [img[left_y][left_x][2],img[left_y][left_x][0],img[left_y][left_x][1]]


