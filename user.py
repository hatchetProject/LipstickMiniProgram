

INDEX_DIR = "IndexFiles.index"

import ImageSearch
import commandSearch
import Color
from MySQLdb import *
import MySQLdb


import web
from web import form
import urllib2
import sys, os, lucene
import jieba
import cv2
from numpy import *
import os
import dlib
import math
import face_recognition
import numpy as np
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.search import SortField
from org.apache.lucene.search import Sort
from org.apache.lucene.search import NumericRangeQuery
from globals import vm_env
##Mysqldb not imported

## center(RBG)(196.147,118.84,120.906)
def get_face_information(image): ##face color
    img=image
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
    

class user:  ##5
    def __init__(self,name):
        ##localhost
        db = MySQLdb.connect("localhost", "root", "980814", "TESTDB", charset='utf8' )
        cursor = db.cursor()
        ##
        ##
        sql = "SELECT * FROM USER \
       WHERE NAME = '%s'" % (name)
        cursor.execute(sql)
        result = cursor.fetchall()
	result=result[0]
        ##
        if len(result)!=0: ##
            self.name=result[0]
            ##self.sex=result[1]
            self.age=result[1]
            self.face=result[2]
            self.face_light=result[3].split('\t')
            self.recommand=result[4].split('\t') ##
            self.recommand_List=result[5].split('\t')
            self.like_List=result[6].split('\t')
	db.close()

    def SearchByImage(self,Image):
        res=ImageSearch(Image)


    def SearchByCommand(self,command): ##
        ##
        res=CommandSearch(command)

    def SearchByRGB(self,lip,recommandList): ##RBG
        f=open('rbg.txt','r')##
        minn=1111111111111
        minkey=0
        for i in f.readlines():
            num=i.strip('\n').split('\t')
            r=int(num[1])
            b=int(num[2])
            g=int(num[3])
            if num[0] not in recommandList:
                dlt=(lip[0]-r)*(lip[0]-r)+(lip[1]-b)*(lip[1]-b)+(lip[2]-g)*(lip[2]-g)
                if dlt<minn:
                    minn=dlt
                    minkey=num[0]
        f.close()
        return minkey
    ##
    def recommand_get_absolute(self): ##OK
        absolute_lip=[]
        absolute_lip.append(float(self.recommand[0])+196.147)
        absolute_lip.append(float(self.recommand[1])+118.84)
        absolute_lip.append(float(self.recommand[2])+120.906)
        return absolute_lip

    
    ##
    ##
    def getRelative(self,recommandLip): ##OK
        relative=[]
        relative.append(float(recommandLip[0])-196.147)
        relative.append(float(recommandLip[1])-118.84)
        relative.append(float(recommandLip[2])-120.906)
        return relative
    
    def RecommandBySelf(self): ##
        f=open('key.txt','r')
        LipStore=f.read().split('\n')
        g=open('rbg.txt','r')
        Lip=g.read().split('\n')
	Like = 1
        ##
        recommandLip=LipStore[int(self.recommand[3])-1]
        ## Write_Back to UI
        ## 
        if (Like):
            attitude=1
        else:
            attitude=-1
        Relative=self.getRelative(self.recommand)
        if len(self.recommand_List)==5:
            self.recommand_List.append(self.recommand[3])
            del self.recommand_List[0]
            self.like_List.append(str(attitude))
            del self.like_List[0]
        else:
            self.recommand_List.append(self.recommand[3])
            self.like_List.append(str(attitude))
        r=0
        b=0
        g=0
        for i in range(len(self.recommand_List)):
            r+=int(self.like_List[i])*float(int(Lip[int(self.recommand_List[i])-1].split('\t')[1])-196.147)
            b+=int(self.like_List[i])*float(int(Lip[int(self.recommand_List[i])-1].split('\t')[2])-118.84)
            g+=int(self.like_List[i])*float(int(Lip[int(self.recommand_List[i])-1].split('\t')[3])-120.906)
        r=float(r)/len(self.recommand_List)
        b=float(b)/len(self.recommand_List)
        g=float(g)/len(self.recommand_List)
        self.recommand[0]=str(r)
        self.recommand[1]=str(b)
        self.recommand[2]=str(g)    
        #
        now_Lip=self.recommand_get_absolute() 
        res=self.SearchByRGB(now_Lip,self.recommand_List)
        ##
        self.recommand[3]=res ##
        strr='\t'
        re=strr.join(self.recommand)
        re_List=strr.join(self.recommand_List)
        li_List=strr.join(self.like_List)
        ##


        db = MySQLdb.connect("localhost", "root", "980814", "TESTDB", charset='utf8' )
        cursor = db.cursor()
        sql = "UPDATE USER SET RECOMMEND = '%s' WHERE name = '%s'" % (re,self.name)
        cursor.execute(sql)
       # 
        db.commit()
        sql = "UPDATE USER SET RECOMMEND_LIST = '%s' WHERE name = '%s'" % (re_List,self.name)
        cursor.execute(sql)
       # 
        db.commit()
        sql = "UPDATE USER SET LIKE_LIST = '%s' WHERE name = '%s'" % (li_List,self.name)
        cursor.execute(sql)
       # 
        db.commit()
        db.close()
        f.close()
        return 0

    def UserSearch(self,image,age): ##
        face=get_face_information(image)
        db = MySQLdb.connect("localhost", "root", "980814", "TESTDB", charset='utf8' )
        cursor = db.cursor()
        sql = "SELECT FACE_LIGHT,RECOMMEND FROM USER "
        cursor.execute(sql)
        results = cursor.fetchall()
        minn=1111111111111
        minre=""
        for i in results:
            re_face=i[0].split('\t')
            dlt=(float(face[0])-float(re_face[0]))*(float(face[0])-float(re_face[0]))+(float(face[1])-float(re_face[1]))*(float(face[1])-float(re_face[1]))+(float(face[2])-float(re_face[2]))*(float(face[2])-float(re_face[2]))
            if dlt<minn:
                minn=dlt
                minre=i[1]
        key=minre.split('\t')[3]
        return key
     
    def RecommandByOthers(self,face_image,age): ##
        res=self.UserSearch(face_image,age)
        f=open('key.txt','r')
        LipStore=f.read().split('\n')
        recommandLip=LipStore[int(res)-1]
	##print recommandLip

    def TryColorBySelf(self,key):
        ##
        face=cv2.imread(self.face)
        res_img=Color(face,key)
        
        
    def TryColorByOthers(self,img,key):
        ##
        res_ima=Color(img,key)
    
    def run(self): ##
	return 0
