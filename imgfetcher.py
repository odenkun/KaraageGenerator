# -*- coding:utf-8 -*-
import urllib2
import json
import numpy
import cv2
#urllib2の取得でリダイレクトさせないためのハンドラ
import unredir

class ImgFetcher:
    def fetch(self,linkArray):
        opener = urllib2.build_opener(unredir.UnFollowRedirectHandler())
        urllib2.install_opener(opener)
        #返却する検索結果の画像配列
        resultImages = []
        for itemLink in linkArray:
            print 'fetching ' + itemLink
            try:
                #リンク先の画像を取得
                image = urllib2.urlopen(itemLink)
                #取得に成功したか？
                if image.getcode() == 200:
                    #opencvで読み込めるように変換
                    element = numpy.asarray(bytearray(image.read()),dtype='uint8')
                    element = cv2.imdecode(element, cv2.IMREAD_UNCHANGED)
                    #結果の配列に追加
                    resultImages.append(element)
                    print 'success ' + itemLink
                else:
                    #エラーが起きたリンクをログ出力
                    print 'redirected ' + str(image.getcode) +' ' + itemLink
            except Exception, e:
                print 'error ' + str(e) + ' ' + itemLink

        return resultImages
