# -*- coding: utf-8 -*-

import feedparser.feedparser

class GooHelper(object):
    @staticmethod
    def get_words():

        # gooキーワードランキングをfeedparserで取得する
        words = []
        rss = feedparser.feedparser.parse('http://ranking.goo.ne.jp/rss/keyword/keyrank_all1/index.rdf')

        for entry in rss.entries:
            text = entry.title

            # 半角スペースが含まれるキーワードは除外する
            if text.find(u' ') > 0:
                continue

            words.append(text)

        return words
