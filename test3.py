import math
import face_recognition
import numpy as np
import cv2


def rounde(p):
    if p>255:
        p=255
    if p<0:
        p=0
    return p

def color_RGB(b,g,r,img):
    img2=np.zeros((len(img),len(img[0]),3),dtype=np.uint8)
    for i in range(len(img)):
        for j in range(len(img[0])):
            img2[i][j][0]=int(img[i][j][0])
            img2[i][j][1]=int(img[i][j][1])
            img2[i][j][2]=int(img[i][j][2])
    face_list=face_recognition.face_landmarks(img)
    p=[]
    for k in face_list[0]["top_lip"]:
        p.append([k[0],k[1]])
    pts=np.array(p,np.int32)
    pts=pts.reshape((-1,1,2))
    cv2.fillPoly(img2,[pts],(255,255,0))
    p=[]
    l=[]
    for k in face_list[0]["bottom_lip"]:
        l.append([k[0],k[1]])
    pts=np.array(l,np.int32)
    pts=pts.reshape((-1,1,2))
    cv2.fillPoly(img2,[pts],(255,255,0))
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img2[i][j][0]==255 and img2[i][j][1]==255 and img2[i][j][2]==0:
                p.append((i,j))
    u1=-0.147*r-0.289*g+0.436*b
    v1=0.615*r-0.515*g-0.1*b
    for k in p:
        i=k[0]
        j=k[1]
        y=0.299*int(img[i][j][2])+0.114*int(img[i][j][0])+0.587*int(img[i][j][1])
        y2=y
        u2=u1
        v2=v1
        r_new=y2+1.14*v2
        g_new=y2-0.39*u2-0.58*v2
        b_new=y2+2.03*u2
        r_new=rounde(r_new)
        g_new=rounde(g_new)
        b_new=rounde(b_new)
        img2[i][j][0]=b_new
        img2[i][j][1]=g_new
        img2[i][j][2]=r_new
    return img2
def Color(face,key):
    f=open('rbg.txt','r')
    LipStore=f.read().split('\n')
        ##
    recommandLip=LipStore[key-1]
    recommandLip=recommandLip.strip('\n').split('\t')
    r=int(recommandLip[1])
    b=int(recommandLip[2])
    g=int(recommandLip[3])
    print (b,g,r)
    img2=color_RGB(b,g,r,img)
    return img2
img=cv2.imread('2.jpeg')
#img_79=Color(img,79)
#cv2.imwrite('img_79.jpg',img_79)
#img_215=Color(img,215)
#cv2.imwrite('img_215.jpg',img_215)
#img_483=Color(img,483)
#cv2.imwrite('img_483.jpg',img_483)
#img_221=Color(img,221)
#cv2.imwrite('img_221.jpg',img_221)
img_552=Color(img,552)
cv2.imwrite('img_552.jpg',img_552)
