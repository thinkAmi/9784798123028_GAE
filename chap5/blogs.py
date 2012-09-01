# -*- coding: utf-8 -*-

from google.appengine.ext import db

import avatars

class Blog(db.Model):
    # 主キー：生成時に(key_name=***)として指定
    # 子クラスへの参照は、collection_nameをarticlesとしてあるので、instance.articlesでアクセス可能
    id = db.IntegerProperty(required=True)
    
    avatarId = db.StringProperty()
    avatarName = db.StringProperty()
    avatarImageName = db.StringProperty()
    avatarMessage = db.StringProperty()
    
    destination = db.StringProperty()
    departureDate = db.DateTimeProperty()
    nextPostDate = db.DateTimeProperty()
    
    # Pythonだと独自クラスをListで持つことができない?
    # See: https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses#ListProperty
    # →仕方がないので、現在登録されている記事数へと変更する
    articleCount = db.IntegerProperty()
    
    
class Article(db.Model):
    
    id = db.DateTimeProperty()
    
    #親クラスへの参照
    #親クラスのインスタンスでは、instance.articles のようにして使えば子クラスを取得できる
    blog = db.ReferenceProperty(reference_class=Blog, collection_name='articles')
    
    postDate = db.DateTimeProperty()
    text = db.StringProperty()
    
    pageUrl = db.StringProperty()
    imageUrl = db.StringProperty()