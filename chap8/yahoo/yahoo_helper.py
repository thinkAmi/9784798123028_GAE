# -*- coding: utf-8 -*-
'''参考 http://hujimi.seesaa.net/article/167665131.html'''

import re
import urllib
from xml.dom import minidom


newline = re.compile('\n')


def _encodeURIComponent(str):
    '''参考 http://d.hatena.ne.jp/ruby-U/20081110/1226313786'''
    
    def replace(match):
        return "%" + hex(ord(match.group()))[2:].upper()
    return re.sub(r"([^0-9A-Za-z!'()*\-._~])", replace, str.encode('utf-8'))


class YahooHelper(object):
    def __init__(self, appid):
        self.url = 'http://jlp.yahooapis.jp/DAService/V1/'
        self.appid = appid


    def get_chunk_list(self, sentence):
        f = urllib.urlopen(self.url +
                             'parse?appid=' + self.appid +
                             '&sentence=' + _encodeURIComponent(sentence))
        dom = minidom.parseString(newline.sub('', f.read()))
        
        chunklist = []
        
        for c in dom.getElementsByTagName('Morphem'):
            feature = c.getElementsByTagName('Feature')[0].firstChild.nodeValue
            featureList = feature.split(',')
            chunklist.append(Feature(featureList))

        return chunklist


class Feature(object):
    def __init__(self, featureList):
        self.pos = featureList[0]
        self.posDetail = featureList[1]
        self.surface = featureList[3]
        self.length = len(featureList)