# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Word(db.Model):
    # 主キーは単語そのもの
    # 詳細な品詞
    posDetail = db.StringProperty()
    # 単語を抽出するためのランダムな値
    rand = db.FloatProperty()