# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:19:29 2019

@author: Lobster
"""

from flask import Flask, request, Markup, render_template
from PIL import Image
import pandas as pd
import csv
from k_means import KMEANS


g_cnt = 3   #クラスタ数
flag_word = [0 for k in range(25)]
flag_img = [0 for k in range(265)]
lst_select_2 = None
clst_word_select_2 = None
clst_img_select_2 = None
x = 1

def __init__(self):
    self.reps=[]
    self.dists=[]
    self.clusters=[]
    self.keep_flag_word=True

def Dist(x1, x2): #2点間のユークリッド距離を返す
    _len = 0.0

    for k in range(2):
        _len = _len + (x1[k]-x2[k])**2
    return _len

def Middle(x1, x2): #2点間の中点を返す
    m = (0,0)
    x = (x1[0]+x1[1])/2
    y = (x2[0]+x2[1])/2
    m = (x,y)
    return m

def select_img_1(word, num, group_img, group_word, img): #ワードから近いイメージを3枚探索
    img_select_cnt = 3
    global flag_word
    global flag_img
    i_save = [0 for k in range(g_cnt)]
    _save = [0 for k in range(g_cnt)]

    for k in range(img_select_cnt):
        l_min = 1.0*10**33
        for i in range(0,265):
            if (group_img[i] == group_word[num]):
                if (flag_img[i] == 0):
                    _len = Dist(img[i][:], word[num])
#                    print(i+1 ,_len)
                    if (_len <= l_min):
                        l_min = _len
                        i_save[k] = i
                        _save[k] = i+1
        flag_img[i_save[k]] = 1
    return _save

# def select_img_2(word, num, group_img, group_word, img): #ワードから近いイメージを3枚探索
#     img_select_cnt = 5
#     global flag_word
#     global flag_img
#     i_save = [0 for k in range(5)]
#     _save = [0 for k in range(5)]
#
#     for k in range(img_select_cnt):
#         l_min = 1.0*10**33
#         for i in range(0,265):
#             if (group_img[i] == group_word[num]):
#                 if (flag_img[i] == 0):
#                     _len = Dist(img[i][:], word[num])
# #                    print(i+1 ,_len)
#                     if (_len <= l_min):
#                         l_min = _len
#                         i_save[k] = i
#                         _save[k] = i+1
#         flag_img[i_save[k]] = 1
#     return _save

def select_word_1(word, group): #各クラスタにおいて原点から最も遠いワードを探索
    global flag_word

    i_save = [0 for k in range(g_cnt)]
    for k in range(g_cnt):
        l_max = 1.0*10**-33

        for i in range(len(word)):
            if (group[i] == k):
                if (flag_word[i] == 0):
                    _len = Dist(word[i][:], [0,0])
                    if (_len >= l_max):
                        l_max = _len
                        i_save[k] = i
        flag_word[i_save[k]] = 1
        print (str(k) + " > " + str(word[i_save[k]][:]), "No.",i_save[k])
    return i_save

def select_word_2(word, num, group): #2回目のワードセレクト
    global flag_word

    i_save = [0 for k in range(g_cnt)]
    j_save = [0 for k in range(g_cnt)]
    h_save = [0 for k in range(g_cnt)]
    select = [0 for k in range(g_cnt)]

    #Ⅰ1回目で選ばれたクラスタ内でそのワードと最も遠いワードを探索
    for k in range(g_cnt):
        l_max = 1.0*10**-33
        for i in range(len(word)):
            if (group[i] == group[num]):
                if (flag_word[i] == 0):
                    _len = Dist(word[i][:], word[num])
                    if (_len >= l_max):
                        l_max = _len
                        i_save[k] = i
                        select[0] = i
    flag_word[i_save[k]] = 1
    print (str(k) + " > " + str(word[i_save[k]][:]), "No.",i_save[k])

    #Ⅱi_save[k]から最も遠いワードを探索
    for k in range(g_cnt):
        l_max = 1.0*10**-33
        for j in range(len(word)):
            if (group[j] == group[num]):
                if (flag_word[j] == 0):
                    _len1 = Dist(word[j][:],word[i_save[k]])
                    if (_len1 >= l_max):
                        l_max = _len1 
                        j_save[k] = j
                        select[1] = j
    flag_word[j_save[k]] = 1
    print (str(k) + " > " + str(word[j_save[k]][:]), "No.",j_save[k])

    #ⅢⅠとⅡの中点から最も遠いワードを探索
    middle = Middle(word[j_save[k]],word[i_save[k]])
    for k in range(g_cnt):
        l_max = 1.0*10**-33
        for h in range(len(word)):
            if (group[h] == group[num]):
                if (flag_word[h] == 0):
                    _len1 = Dist(word[h][:], middle)
                    if (_len1 >= l_max):
                        l_max = _len1 
                        h_save[k] = h
                        select[2] = h
    flag_word[h_save[k]] = 1
    print (str(k) + " > " + str(word[h_save[k]][:]), "No.",h_save[k])
    return select
        
app = Flask(__name__)


@app.route('/')
def index():
    print("")

    global x
    x += 1

    lst = pd.read_csv("data100.csv").values.tolist() #csv読み込み
    global lst_select_2
    lst_select_2 = lst
    clustering=KMEANS()

    clustering.Clustering(lst,g_cnt)

    clst = clustering.clusters
    clst_word = clst[0:25]
    clst_img = clst[25:290]
    global clst_word_select_2
    global clst_img_select_2
    clst_word_select_2 = clst_word
    clst_img_select_2 = clst_img

    print("CLST_WORD -> " + str(clst_word))
    print("             "+ "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]")
    print("FLAG_WORD -> "+ str(flag_word))
    
#---クラスタごとの大きさ------------------------------------------------
    cnt0 = 0
    cnt1 = 0
    cnt2 = 0
    
    for i in range(25):
        if (clst_word[i] == 0):
            cnt0 += 1
        if (clst_word[i] == 1):
            cnt1 += 1
        if (clst_word[i] == 2):
            cnt2 += 1
#----------------------------------------------------------------

    flg0 = 0
    flg1 = 0
    flg2 = 0
    
    for i in range(10):
        for i in range(25):
            if (clst_word[i] == 0 and flag_word[i] == 1):
                flg0 += 1
            if (clst_word[i] == 1 and flag_word[i] == 1):
                flg1 += 1
            if (clst_word[i] == 2 and flag_word[i] == 1):
                flg2 += 1    
#         if (x == 2):
# #            flag_word[0]=1
# #            flag_word[7]=1
# #            flag_word[10]=1
#             i_select_1 = select_word_1(lst[0:25], clst_word)
#             return render_template('index.html', type=int, img=i_select_1, len=25)
        i_select_1 = select_word_1(lst[0:25], clst_word)
        print("CLST_WORD -> " + str(clst_word))
        print("             " + "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]")
        print("FLAG_WORD -> " + str(flag_word))
        return render_template('index.html', type=int, img=i_select_1, len=25)

@app.route("/test")
def test1():
    favs = request.values.getlist("que")
    clst_word = clst_word_select_2
    aaa = int(favs[0])
    flag_word[aaa] = 1
    print("SELECT_No. -> "+str(favs))

    cnt0 = 0
    cnt1 = 0
    cnt2 = 0
    
    for i in range(25):
        if (clst_word[i] == 0):
            cnt0 += 1
        if (clst_word[i] == 1):
            cnt1 += 1
        if (clst_word[i] == 2):
            cnt2 += 1
#----------------------------------------------------------------
    flg0 = 0
    flg1 = 0
    flg2 = 0

    for i in range(10):

        for i in range(25):
            if (clst_word[i] == 0 and flag_word[i] == 1):
                flg0 += 1
            if (clst_word[i] == 1 and flag_word[i] == 1):
                flg1 += 1
            if (clst_word[i] == 2 and flag_word[i] == 1):
                flg2 += 1    

    print("")
    print("---select2---")
    i_select_2 = select_word_2(lst_select_2[0:25], int(favs[0]), clst_word)
    print("CLST_WORD -> " + str(clst_word))
    print("             "+ "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]")
    print("FLAG_WORD -> "+ str(flag_word))
    return render_template('index2.html', type=int, img=i_select_2, len=25)
@app.route("/img")
def test2():
    print("")
    clst_img = clst_img_select_2
    clst_word = clst_word_select_2
    favs2 = request.values.getlist("que2")
    print("SELECT_No. -> "+str(favs2))
    i_select_3 = select_img_1(lst_select_2[0:25], int(favs2[0]), clst_img, clst_word, lst_select_2[25:290])

    # for i in range(25):
    #     buff = select_img_2(lst_select_2[0:25], i, clst_img, clst_word, lst_select_2[25:290])
    #     print(buff)

    print(i_select_3)
    return render_template('image.html', type=int, img=i_select_3, value=265)

@app.route("/end")
def end():
    return "End"

if __name__ == '__main__':
    app.run()
