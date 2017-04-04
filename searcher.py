# -*- coding:utf-8 -*-

import os.path
import urllib
import urllib2
import json

class CustomSearch:
    def fetchJSON (self,query,apiKey,searchEngineID):

        API_URL = 'https://www.googleapis.com/customsearch/v1?'

        params = {
            'key': apiKey,
            'q':query.encode('utf-8'),
            'cx': searchEngineID,
            'alt':'json',
            'lr' :'lang_ja',
            'searchType' : 'image'
        }
        #リクエストするURL
        req_url = API_URL + urllib.urlencode(params)
        #リクエストの実行結果
        res = None
        if os.path.exists(query + '.json'):
            print query + '.json exists.'
            res = open(query + '.json','r')
        else:
            print query + '.json does not exist.'
            res = urllib2.urlopen(req_url)

        #結果は文字列なのでJSONオブジェクトに変換
        resObj = json.loads(res.read())
        #結果のJSONを保存
        resout = open(query + '.json','w')
        resout.write(json.dumps(resObj))
        resout.close()
        linkArray = []
        for element in resObj['items']:
            url = element[u'link']
            if element['image']['height'] > 1000 or element['image']['width'] > 1000:
                print 'The raw image is too large to use' + url
                url = element['image']['thumbnailLink']
                continue
            linkArray.append(url)
        return linkArray
