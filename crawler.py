# -*- coding:utf-8 -*-
import urllib2
import json
import cv2
import numpy
import random
from PIL import Image
#CustomSearchAPIで画像検索して画像リンク配列を返却する
import searcher
#画像を取得する
import imgfetcher

def extractBrown(image):
    ret = frame = image
    if frame is None or len(frame.shape) < 3 or frame.shape[2] < 3:
        return None

    cv2.imwrite(str(frame.shape[0]) + '.png',frame)
    if frame.shape[2] == 3:
        print 'image has not alpha channel'
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    # フレームをHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (17,17), 0)
    # 指定した色に基づいたマスク画像の生成
    img_mask = cv2.inRange(hsv, min_brown, max_brown)
    # フレーム画像とマスク画像の共通の領域を抽出する。
    img_color = cv2.bitwise_and(frame, frame, mask=img_mask)
    point = img_color.shape[:2]
    '''
    if point < (300,300):
        randi = random.randint(1,3)
        img_color = cv2.resize(img_color,None, fx= randi, fy= randi)
    '''
    if point > (500,500):
        randf = random.random()
        img_color = cv2.resize(img_color,None, fx= randf, fy= randf)

    return img_color

# 取得する色の範囲を指定する
# 色相、彩度、明度
min_brown = numpy.array([ 6 , 50,40])
max_brown = numpy.array([20, 255, 250])

#検索する文字列
QUERY = None
API_KEY = None
SEARCH_ENGINE_ID = None

linkArray = searcher.CustomSearch().fetchJSON(QUERY,API_KEY,SEARCH_ENGINE_ID)
imgArray = imgfetcher.ImgFetcher().fetch(linkArray)
random.shuffle(imgArray)

pilFrame = Image.fromarray(cv2.imread('under.png', cv2.IMREAD_UNCHANGED))
resultImage = Image.new("RGBA", pilFrame.size, (63, 82, 166, 255))
for i in range(len(imgArray)):
    brownImage = extractBrown(imgArray[i])
    if brownImage is None:
        print 'none'
        continue

    pilOver = Image.fromarray(brownImage)
    canvas = Image.new('RGBA', resultImage.size, (255, 255,255, 0))
    posX = random.randint( 0, 250)
    posY = random.randint( -70, 70)
    canvas.paste(pilOver, (posX, posY) )
    canvas = canvas.rotate(random.randint(0,360))
    if random.randint(0,2) == 0:
        canvas.transpose(Image.FLIP_LEFT_RIGHT)
    if random.randint(0,2) == 0:
        canvas.transpose(Image.FLIP_TOP_BOTTOM)
    resultImage = Image.alpha_composite(resultImage, canvas)

resultImage = Image.alpha_composite(resultImage, pilFrame)
cv2.imwrite('teagra.png',numpy.asarray(resultImage))
