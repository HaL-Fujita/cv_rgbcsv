
import cv2
import os
import numbers
import random

import wave
import numpy as np
from matplotlib import pylab as plt
import struct

a = 1     #振幅
fs = 8000 #サンプリング周波数
f0 = 440  #周波数
sec = 1   #秒
# swav=[]
wav=[]
# for n in np.arange(fs * sec):
#     #サイン波を生成
#     s = a * np.sin(2.0 * np.pi * f0 * n / fs)
#     swav.append(s)
# #サイン波を表示
# plt.plot(swav[0:100])
# plt.show()
# #サイン波を-32768から32767の整数値に変換(signed 16bit pcm)
# swav = [int(x * 32767.0) for x in swav]
# #バイナリ化
# binwave = struct.pack("h" * len(swav), *swav)
# #サイン波をwavファイルとして書き出し
# w = wave.Wave_write("output.wav")
# p = (1, 2, 8000, len(binwave), 'NONE', 'not compressed')
# w.setparams(p)
# w.writeframes(binwave)
# w.close()


# 対象画像読み込み

PICNAME = "Fujita.png"
img = cv2.imread(PICNAME,cv2.IMREAD_COLOR)

height, width, channels = img.shape[:3]
imgsize = range(int(width / 20))

# 対象範囲を切り出し
boxFromX = 0 #対象範囲開始位置 X座標
boxFromY = 0 #対象範囲開始位置 Y座標
boxToX = 100 #対象範囲終了位置 X座標
boxToY = height #対象範囲終了位置 Y座標
# y:y+h, x:x+w　の順で設定

imgBox = [[] for _ in imgsize]
rgbhsv = []
octerve = []


for i in imgsize:
    imgBox[i] = img[boxFromY: boxToY, boxFromX: boxToX]

    # RGB平均値を出力
    # flattenで一次元化しmeanで平均を取得 
    b = imgBox[i].T[0].flatten().mean()
    g = imgBox[i].T[1].flatten().mean()
    r = imgBox[i].T[2].flatten().mean()

    # RGB平均値を取得

    # BGRからHSVに変換
    imgBoxHsv = [[] for _ in imgsize]
    imgBoxHsv[i] = cv2.cvtColor(imgBox[i],cv2.COLOR_BGR2HSV)

    # HSV平均値を取得
    # flattenで一次元化しmeanで平均を取得
    h = imgBoxHsv[i].T[0].flatten().mean()
    s = imgBoxHsv[i].T[1].flatten().mean()
    v = imgBoxHsv[i].T[2].flatten().mean()
    
    # sv= abs(s-v)
    # print("sv: %.2f" % (sv))
    culc = abs(h-90)*s*v/500
    octerve.append(culc)
    boxToX = boxToX + 20 #対象範囲終了位置 X座標

swav =[]
for j in range(len(octerve)):   
    print("octervej: %.2f" % octerve[j])
        
    for n in np.arange(fs * sec):
        #サイン波を生成
        s = a * np.sin(2.0 * np.pi * octerve[j] * (n+1)/ fs)
        swav.append(s)
    #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
    swav = [int(x * 32767.0) for x in swav]
    #バイナリ化
    binwave = struct.pack("h" * len(swav), *swav)
    #サイン波をwavファイルとして書き出し
    w = wave.Wave_write("output%.2f.wav" % j)
    p = (1, 2, 8000, len(binwave), 'NONE', 'not compressed')
    w.setparams(p)
    w.writeframes(binwave)
    w.close()
    swav = []
