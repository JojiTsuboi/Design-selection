# coding: UTF-8


from numpy import *
import numpy as np
from matplotlib.font_manager import FontProperties
# from matplotlib.pyplot import figure, show
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import csv

# タブ区切りデータ読み込み
csvfile = open('data2.txt')#分析対象データファイル
dlist = []#データ2次元リスト
slist = []#サンプル名称リスト
tmp =  []
hlist =  []#ヘッダーリスト

if csvfile != None:
    n = 0
    for row in csv.reader(csvfile):
        for col in row:
            Lt = col.strip().split('\t')
            if n == 0:
                tmp = Lt
                hlist = tmp[1:]
            else:
                cols = Lt
                slist.append(cols[0])
                dlist.append([float(str) for str in cols[1:]])
            n += 1
csvfile.close
HN = vstack(hlist)
SN = vstack(slist)
R = vstack(dlist)
print (u"--分析対象となるデータ行列:R--")
print (R)

R_num_row = len(R)      #サンプルの数＝行数
R_num_col = size(R[0])  #カテゴリの数＝列数
S = [0 for i in range(R_num_row)]
C = [0 for i in range(R_num_col)]

print (u"--カテゴリごとの点数が対角にある行列の逆行列:CI--")
for m in range(0,R_num_col):
    sum = 0
    for n in range(0,R_num_row):
        sum += R[n,m]
    C[m] = sum
CI = mat(diag(C)).I#対角化・逆行列
print (CI)

print (u"--サンプルごとの点数の平方根が対角にある行列の逆行列:SI--")
for n in range(0,R_num_row):
    sum = 0
    for m in range(0,R_num_col):
        sum += R[n,m]
    S[n] = sqrt(sum)

SI = mat(diag(S)).I #対角化・逆行列
print (SI)

print (u"--データ行列Rの転置行列:RT--")
RT = R.T
print (RT)

print (u"--SI*R*CI*RT*SI*v=r2*vを満たす固有値・固有ベクトル--")
X = SI*R*CI*RT*SI
v,r2,vh = linalg.svd(X) #特異値分解のメソッドを使用する
print (u"固有値:r2")
print (r2)

r2 = r2[1:]#固有値1をスライスして削除
np.set_printoptions(precision=4, floatmode='fixed', suppress=True)

print (u"寄与率:r3")
rs = r2.sum()
r3 = [0]*size(r2)
for n in range(0,size(r2)):
    r3[n] = r2[n]/rs
print (r3)

print (u"固有ベクトル:v")
print (v)

print (u"単相関関係数:r")
r = sqrt(r2)
print (r)

print (u"--サンプルデザイン--")
x1 = sqrt(R.sum())*v[:,1:]#固有ベクトルに長さを乗する
x1 = SI*x1
print (x1)

print (u"--感性ワード--")
y1 = CI*R.T*x1
y2 = zeros((len(y1),size(y1[0])))
for j in range(0,size(y1[0])):
    y2[:,j:j+1] = y1[:,j]/r[j]
y2 = mat(y2)
print (y2)

print (u"--散布図表示（第1成分X軸，第2成分Y軸）--")
s_score_x = zeros((1,1))
s_score_y = zeros((1,1))
s_score_z = zeros((1,1))
c_score_x = zeros((1,1))
c_score_y = zeros((1,1))
c_score_z = zeros((1,1))

s_score_x = np.array(x1[:,0])#u"--サンプルデザインX軸--"
s_score_y = np.array(x1[:,1])#u"--サンプルデザインY軸--"
s_score_z = np.array(x1[:,2])#u"--サンプルデザインz軸--"
c_score_x = np.array(y2[:,0])#u"--感性ワードX軸--"
c_score_y = np.array(y2[:,1])#u"--感性ワードY軸--"
c_score_z = np.array(y2[:,2])#u"--感性ワードz軸--"

# 一次元配列へreshape
X_s = s_score_x.reshape(1, s_score_x.shape[0])[0,:]
Y_s = s_score_y.reshape(1, s_score_y.shape[0])[0,:]
Z_s = s_score_z.reshape(1, s_score_z.shape[0])[0,:]
X_c = c_score_x.reshape(1, c_score_x.shape[0])[0,:]
Y_c = c_score_y.reshape(1, c_score_y.shape[0])[0,:]
Z_c = c_score_z.reshape(1, c_score_z.shape[0])[0,:]

fig = plt.figure()
ax = Axes3D(fig)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

#MSゴシック
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\msgothic.ttc')

# 感性ワードの脚注
for i in range(25):
    ax.text(X_c[i], Y_c[i], Z_c[i], hlist[i], size=10, zorder=1, color='k', fontproperties = fp)
# サンプルデザインの脚注
for i in range(265):
    ax.text(X_s[i], Y_s[i], Z_s[i], slist[i], size=10, zorder=1, color='k')

ax.plot(X_s,Y_s,Z_s,marker="o",linestyle='None')
ax.plot(X_c,Y_c,Z_c,marker="o",linestyle='None')

plt.show()

