import cv2
import numbers
import random
import cgi
import sys
import io
import wave
import numpy as np

import cgi
import base64

from matplotlib import pylab as plt
import struct

import os

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime as dt

a = 1     #振幅
fs = 8000 #サンプリング周波数
f0 = 440  #周波数
sec = 0.1   #秒
wav=[]

img = "static/images/parrot.png" 
img = cv2.imread(img,cv2.IMREAD_COLOR)
img = cv2.resize(img, dsize=(1000, 1000))
height, width, channels = img.shape[:3]
imgsize = range(int(width / 10))
# 対象範囲を切り出し
boxFromX = 0 #対象範囲開始位置 X座標
boxFromY = 0 #対象範囲開始位置 Y座標
boxToX = 10 #対象範囲終了位置 X座標
boxToY = height #対象範囲終了位置 Y座標
# y:y+h, x:x+w　の順で設定
imgBox = [[] for _ in imgsize]
octerve = []

for i in imgsize:
    imgBox[i] = img[boxFromY: boxToY, boxFromX: boxToX]

    # BGRからHSVに変換
    imgBoxHsv = [[] for _ in imgsize]
    imgBoxHsv[i] = cv2.cvtColor(imgBox[i],cv2.COLOR_BGR2HSV)

    # HSV平均値を取得
    # flattenで一次元化しmeanで平均を取得
    h = imgBoxHsv[i].T[0].flatten().mean()
    s = imgBoxHsv[i].T[1].flatten().mean()
    v = imgBoxHsv[i].T[2].flatten().mean()  

    culc = abs(h-90)*s*v/500
    octerve.append(culc)
    boxToX = boxToX + 10 #対象範囲終了位置 X座標
swav = [[] for _ in range(len(octerve))]
for j in range(len(octerve)):   
    print("octervej: %.2f" % j)
    for n in np.arange(fs * sec):
        #サイン波を生成
        s = a * np.sin(2.0 * np.pi * octerve[j] * (n+1)/ fs)
        swav[j].append(s)
    #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
    swav[j]= [int(x * 32767.0) for x in swav[j]]
    wav.extend(swav[j])
#バイナリ化
binwave = struct.pack("h" * len(wav), *wav)
#サイン波をwavファイルとして書き出し
w = wave.Wave_write("output.wav")
p = (1, 2, 8000, len(wav), 'NONE', 'not compressed')
w.setparams(p)
w.writeframes(binwave)
w.close()
