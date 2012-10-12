# -*- coding: utf-8 -*-

import re
import logging

from google.appengine.api import urlfetch
from lxml import etree

import api_config



def _encodeURIComponent(str):
    '''参考 http://d.hatena.ne.jp/ruby-U/20081110/1226313786'''
    
    def replace(match):
        return "%" + hex(ord(match.group()))[2:].upper()
    return re.sub(r"([^0-9A-Za-z!'()*\-._~])", replace, str.encode('utf-8'))


class YahooHelper(object):
    def get_furigana(self, word):
        # ルビ振りサービスを呼び出す
        response = urlfetch.fetch(
                                  'http://jlp.yahooapis.jp/FuriganaService/V1/furigana?appid='
                                  + api_config.Yahoo.APPLICATION_ID
                                  + '&sentence='
                                  + _encodeURIComponent(word)
                                  )

        # 取得した単語を１つずつ処理する
        results = []
        xml = etree.fromstring(response.content)
        entries = xml.xpath('//xs:Result/xs:WordList/xs:Word', namespaces={'xs':'urn:yahoo:jp:jlp:FuriganaService'})

        for entry in entries:
            # xpathはlistで戻ってくる
            furigana = entry.xpath('./xs:Furigana/text()', namespaces={'xs':'urn:yahoo:jp:jlp:FuriganaService'})
            if furigana[0] != '':
                # ふりがながあれば利用する
                results.append(furigana[0])

            else:
                # ふりがながない(英数字など)場合は、単語をそのまま利用する
                alphameric = entry.xpath('./xs:Word/xs:Surface/text()', namespaces={'xs':'urn:yahoo:jp:jlp:FuriganaService'})
                results.append(alphameric)

        return ''.join(results)


    # 関連検索ワードを最大50件取得する
    def get_hints(self, word):
        # 関連検索ワードサービスを呼び出す
        response = urlfetch.fetch(
                                  'http://search.yahooapis.jp/AssistSearchService/V1/webunitSearch?appid='
                                  + api_config.Yahoo.APPLICATION_ID
                                  + '&query='
                                  + _encodeURIComponent(word)
                                  + '&results=50'
                                  )

        # 関連検索ワードを１つずつ処理する
        hints = []
        xml = etree.fromstring(response.content)
        entries = xml.xpath('//xs:Result/text()', namespaces={'xs':'urn:yahoo:jp:srchunit'})

        for entry in entries:
            goodHint = self._get_good_hint(word, entry)

            if goodHint != None and not(goodHint in hints):
                # 新しい検索ワードであれば、返り値候補に追加する
                hints.append(goodHint)

                if len(hints) >= 16:
                    # 16個ヒントを用意したら、結果を返す
                    return hints

        return hints


    def _get_good_hint(self, word, result):
        # 関連検索ワードは、半角スペースで区切られているので、分離しておく
        hintWords = result.split(' ')

        if len(hintWords) <= 1:
            # 短すぎるヒントのため、不適切
            return None

        # 答えと一致しないヒントを、良いヒントとする
        for hintWord in hintWords:
            if word != hintWord:
                return hintWord

        # ヒントが得られなかった場合は、不適切なヒント
        return None



