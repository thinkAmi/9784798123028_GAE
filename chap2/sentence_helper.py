#-*- coding: utf-8 -*-

import random

class SentenceHelper(object):
    __whenList = [u'さっき', u'昨日', u'あれはもう３年も昔', u'紀元前', u'ジュラ紀']
    __whereList = [u'自宅で', u'近くの居酒屋で', u'世界のまんなかで', u'追い込み中のプロジェクトで', u'木星で']
    __whoList = [u'わたしが', u'あなたが', u'オヤジが', u'あこがれのアイドルが', u'神が']
    __whatList = [u'新しいソートアルゴリズムを発見した', u'イグノーベル賞を受賞した', u'悟りを開いた', u'こけた', u'十円ひろった']


    @classmethod
    def make_sentence(self, when, where, who, what):
        when = self.__choice(self.__whenList) if when == '' else when
        where = self.__choice(self.__whereList) if where == '' else where
        who = self.__choice(self.__whoList) if who == '' else who
        what = self.__choice(self.__whatList) if what == '' else what
	
        return when + where + who + what
	
	
    @staticmethod
    def __choice(lists):
        randomIndex = random.randint(0, len(lists) - 1)
        return lists[randomIndex]
