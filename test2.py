import user
import cv2
import MySQLdb

user1=user.user("a")
user1.RecommandBySelf()
img=cv2.imread('1.jpg')
user1.RecommandByOthers(img,20)
