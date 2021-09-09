
import cv2
import os
import numbers
import random

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
    
    sv= abs(s-v)
    print("sv: %.2f" % (sv))
    octerve = abs(h-90)*s*v/500
    # HSV平均値を出力
    # uHeは[0,179], Saturationは[0,255]，Valueは[0,255]
    
    print("octerve: %.2f" % (octerve))

    rgbhsv.append([r,g,b,h,s,v])
    boxToX = boxToX + 20 #対象範囲終了位置 X座標
