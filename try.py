from math import *

def matchcolor(r, g, b):
    res = []
    u = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    v = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    minimum = sqrt(255**2 *3)
    std=open('rbg.txt','r')
    for i in std.readlines():
        ttt=i.strip('\n').split('\t')
        rt=int(ttt[1])
        bt=int(ttt[2])
        gt=int(ttt[3])
        keyt=int(ttt[0])
        u1 = -0.1687 * rt - 0.3313 * gt + 0.5 * bt + 128
        v1 = 0.5 * rt - 0.4187 * gt - 0.0813 * bt + 128
        tmp = sqrt((u - u1) ** 2 + (v - v1) ** 2) 
        res.append((tmp,keyt))
        res.sort()
        res = res[:5]
    return res
res=matchcolor(200,124,111)
print res
