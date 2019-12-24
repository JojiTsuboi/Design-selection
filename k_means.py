# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 14:43:19 2019

@author: Lobster
"""

import numpy as np
import csv

class KMEANS:

    def __init__(self):
        self.reps=[]
        self.dists=[]
        self.clusters=[]
        self.keep_flag=True

    # c_data: クラスタリング対象データ
    # k: クラスタ数
    def Clustering(self, c_datas, k):
        # 代表点を初期化
        self.RepInit(c_datas, k)

        while self.keep_flag:
            # 代表点と点の距離を計算
            self.ClusterDist(c_datas)

            # 所属クラスタを更新
            self.ClusterUpdate()

            # 代表点を更新
            self.RepUpdate(c_datas)
            
        #f = open('output50.csv', 'w')
        #writer = csv.writer(f, lineterminator='\n')
            
        # データをリストに保持
        csvlist = self.clusters
            
            
        # 出力
        #writer.writerow(csvlist)

    # クラスタ代表点の初期化 + 代表点と各点の距離と所属クラスタを格納するリストの初期化
    def RepInit(self, c_datas, k):
        for i in range(k):
            self.reps.append(list(np.random.rand(len(c_datas[0]))))
        self.dists = [[-1 for j in range(len(self.reps))] for i in range(len(c_datas))]
        self.clusters=[-1 for i in range(len(c_datas))]

    # 代表点と点の距離を計算
    def ClusterDist(self, c_datas):
        for (i, c_data) in enumerate(c_datas):
            for (j, rep) in enumerate(self.reps):
                # 各点の代表点との距離を計算
                self.dists[i][j] = self.Dist(c_data, rep)

    # 二点間の距離を計算
    def Dist(self, x1, x2):
        return np.linalg.norm(np.array(x1) - np.array(x2))

    # 所属クラスタ更新
    def ClusterUpdate(self):
        flag=False
        for (i, dist) in enumerate(self.dists):
            # クラスタ更新があった場合はwhileループのフラグをTrueに維持
            if self.clusters[i] != np.argmin(dist):
                flag=True
            # 距離のリストから最小値の引数を得る
            self.clusters[i] = np.argmin(dist)
        self.keep_flag=flag

    # クラスタの代表点を更新
    def RepUpdate(self, c_datas):
        for c_num in range(len(self.reps)):
            cluster_points=[]
            for i, (cluster, c_data) in enumerate(zip(self.clusters,c_datas)):
                if cluster == c_num:
                    # clauster_pointsにc_numクラスタの点を追加
                    cluster_points.append(c_datas[i])
            if len(cluster_points) is 0:
                cluster_points.append(self.reps[c_num])
            # 点の平均を求め代表点を更新
            self.reps[c_num] = list(np.array(cluster_points).mean(axis=0))
            
