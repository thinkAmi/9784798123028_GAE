# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Alarm(db.Model):
	#主キー：生成時に(key_name='emailアドレス')として指定してあげる
	email = db.StringProperty(required=True)
	
	nickname = db.StringProperty()
	wakeupDate = db.DateTimeProperty()
	count = db.IntegerProperty()
