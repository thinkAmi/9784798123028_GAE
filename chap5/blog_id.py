# -*- coding: utf-8 -*-

from google.appengine.ext import db

class BlogId(db.Model):

    currentId = db.IntegerProperty(required=True)
