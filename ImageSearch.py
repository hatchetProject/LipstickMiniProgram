#Lip-color matching

import dlib
import math

def initial(folder):
    for brand in folder:
        f = open(brand + '/' + brand + '.txt', 'r')
        f2 = open(brand + '/' + 'color.txt', 'w')
        for k in range(len(os.listdir(brand + '/')) - 2):
            if brand=='ysl':
                img = cv2.imread(brand + '/' + str(k + 1) + '.jpg', cv2.IMREAD_COLOR)
            else:
                img = cv2.imread(brand + '/' + str(k + 1) + '.png', cv2.IMREAD_COLOR)
            img = cv2.GaussianBlur(img, (5,5), 0.1)
            rbins = [0]*256
            gbins = [0]*256
            bbins = [0]*256
            for i in range(len(img)):
                for j in range(len(img[0])):
                    tmp = img[i][j]
                    tmpb, tmpg, tmpr = int(round(tmp[0])), int(round(tmp[1])), int(round(tmp[2]))
                    if tmpb==0 and tmpg==0 and tmpr==0:
                        continue
                    rbins[tmpr] += 1
                    gbins[tmpg] += 1
                    bbins[tmpb] += 1
            r = rbins.index(max(rbins))
            g = gbins.index(max(gbins))
            b = bbins.index(max(bbins))
            f2.write(str(r) + '\t' + str(g) + '\t' + str(b) + '\n')
        f.close()
        f2.close()

def stdcolor(folder):
    std = {}
    for brand in folder:
        f = open(brand + '/' + brand + '.txt', 'r')
        f2 = open(brand + '/' + 'color.txt', 'r')
        for line in f2:
            tmp = line.split()
            tmp2 = f.readline().split('\t')
	    for  i in range(len(tmp2)):
		if brand=='dior' or brand=='ysl':
		    tmp2[i]=tmp2[i].decode('gbk')
		else:
		    tmp2[i]=tmp2[i].decode('utf8')
            std[tmp2[0]] = [(int(tmp[0]), int(tmp[1]), int(tmp[2])), tmp2[1:]]
        f.close()
        f2.close()
    return std

def lipscolor(img):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") 
    faces = detector(img, 1)
    feature = []
    for face in faces:
        feature.append(predictor(img, face))
    xs = []
    ys = []
    for i in range(48,68):
        xs.append(feature[0].part(i).x)
        ys.append(feature[0].part(i).y)
    r1 = 0
    g1 = 0
    b1 = 0
    r2 = 0
    g2 = 0
    b2 = 0
    count1 = 0
    count2 = 0
    for i in [1,2,4,5]:
        for j in [13,14,15]:
            d = math.sqrt((ys[i] - ys[j]) ** 2 + (xs[i] - xs[j]) ** 2)
            theta = 90 if xs[i] == xs[j] else math.atan((ys[i] - ys[i]) / float(xs[i] - xs[j]))
            th = max(abs(d*math.cos(theta)), abs(d * math.sin(theta)))
            for k in range(1,int(th) + 1):
                b1 += img[int(round(ys[i] + k * math.sin(theta)))][int(round(xs[i] + k * math.cos(theta)))][0]
                g1 += img[int(round(ys[i] + k * math.sin(theta)))][int(round(xs[i] + k * math.cos(theta)))][1]
                r1 += img[int(round(ys[i] + k * math.sin(theta)))][int(round(xs[i] + k * math.cos(theta)))][2]
                count1 += 1
    for i in [7,8,10,11]:
        for j in [17,19]:
            d = math.sqrt((ys[i] - ys[j]) ** 2 + (xs[i] - xs[j]) ** 2)
            theta = 90 if xs[i] == xs[j] else math.atan((ys[i] - ys[i]) / float(xs[i] - xs[j]))
            th = max(abs(d*math.cos(theta)), abs(d * math.sin(theta)))
            for k in range(1,int(th) + 1):
                b2 += img[int(round(ys[i] + k * math.sin(theta)))][int(round(xs[i] + k * math.cos(theta)))][0]
                g2 += img[int(round(ys[i] + k * math.sin(theta)))][int(round(xs[i] + k * math.cos(theta)))][1]
                r2 += img[int(round(ys[i] + k * math.sin(theta)))][int(round(xs[i] + k * math.cos(theta)))][2]
                count2 += 1
    r = ((r1 / count1) * 0.6 + (r2 / count2) * 0.4) * 1.01         
    g = ((g1 / count1) * 0.6 + (g2 / count2) * 0.4) * 0.68
    b = ((b1 / count1) * 0.6 + (b2 / count2) * 0.4) * 0.7
    return int(r),int(g),int(b)

##def matchcolor(r, g, b):
#    res = []
#    u = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
#    v = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
#    minimum = sqrt(255**2 *3)
#    std=open('rbg.txt','r')
#    for i in std:
#        ttt=std.strip('\n').split('\t')
#        rt=ttt[1]
#        bt=ttt[2]
#        gt=ttt[3]
#        keyt=ttt[0]
#        u1 = -0.1687 * rt - 0.3313 * gt + 0.5 * bt + 128
#        v1 = 0.5 * rt - 0.4187 * gt - 0.0813 * bt + 128
#        tmp = sqrt((u - u1) ** 2 + (v - v1) ** 2) 
#        res.append(tmp,keyt)
#        res.sort()
#    return res     
def matchcolor(r, g, b):
    res = []
    u = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    v = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    minimum = math.sqrt(255**2 *3)
    std=open('rbg.txt','r')
    for i in std.readlines():
        ttt=i.strip('\n').split('\t')
        rt=int(ttt[1])
        bt=int(ttt[2])
        gt=int(ttt[3])
        keyt=int(ttt[0])
        u1 = -0.1687 * rt - 0.3313 * gt + 0.5 * bt + 128
        v1 = 0.5 * rt - 0.4187 * gt - 0.0813 * bt + 128
        tmp = math.sqrt((u - u1) ** 2 + (v - v1) ** 2) 
        res.append((tmp,keyt))
        res.sort()
    return res
def preprocessing():
    orb = cv2.ORB()
    for brand in folder:
        f = open(brand + '/' + brand + '.txt', 'r')
        t = len(os.listdir(brand + '/')) - 1
        for k in range(t):
            f2 = open('dataset/' + brand + str(k + 1) + '.txt', 'w')
            img = cv2.imread(brand + '/' + str(k + 1) + '.jpg', cv2.IMREAD_COLOR)
            img = cv2.GaussianBlur(img, (5,5), 0.1)
            tmp = f.readline()
            f2.write(tmp)
            des = orb.detectAndCompute(img, None)[1]
            for i in des:
                for j in i:
                    f2.write(str(j) + '\t')
                f2.write('\n')
            f2.close()
        f.close()


def initialize():
    lipstick = {}
    for i in os.listdir('dataset/'):
        f = open('dataset/' + i, 'r')
        key = f.readline()
        value = []
        for j in f.readlines():
            tmp = j.split()
            temp = []
            for k in tmp:
                temp.append(int(k))
            value.append(array(temp,dtype='uint8'))
        lipstick[key] = array(value)
    return lipstick


def match(img, dataset): ##
    orb = cv2.ORB()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    img = cv2.GaussianBlur(img, (5,5), 0.1)
    tdes = orb.detectAndCompute(img, None)[1]
    res = []
    minimum = 100000000
    for i in dataset:
        tmp = 0
        matches = bf.match(tdes, dataset[i])
        for j in range(len(matches)):
            tmp += matches[j].distance
        if (tmp == minimum) or (tmp > minimum and tmp < minimum + 10):
            res.append(i)
        elif tmp < minimum -10:
            res = [i]
            minimum = tmp
        elif tmp < minimum:
            res.insert(0, i)
            minimum =tmp 
    return res

detector = dlib.get_frontal_face_detector()
def imageSearch(Image):
    img = Image
    r,g,b = lipscolor(img)
    res = matchcolor(r,g,b)
    res = res[:5]
    return res














