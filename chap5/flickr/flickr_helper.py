# -*- coding: utf-8 -*-

import urllib
from google.appengine.api import urlfetch
from xml.dom import minidom


API_URL = 'http://api.flickr.com/services/rest/?'
API_KEY = '<your api key>'
API_METHOD = 'flickr.photos.search'
LICENSE = '1,2,3,4,5,6'



class FlickrHelper(object):

    farm = ''
    server = ''
    id = ''
    secret = ''
    owner = ''
    
    
    def fetch(self, keywords):
    
        url = self.build_search_url(keywords)
        result = urlfetch.fetch(url)
        dom = minidom.parseString(result.content)
        photos = dom.getElementsByTagName("photo")
        
        for photo in photos:
            self.farm = photo.getAttribute("farm")
            self.server = photo.getAttribute("server")
            self.id = photo.getAttribute("id")
            self.secret = photo.getAttribute("secret")
            self.owner = photo.getAttribute("owner")
            
            return
        
        
        
    def build_search_url(self, keywords):
        builder = []
        builder.append(API_URL)
        builder.append('method=')
        builder.append(API_METHOD)
        builder.append('&format=rest')
        builder.append('&api_key=')
        builder.append(API_KEY)
        builder.append('&per_page=1')
        builder.append('&license=')
        builder.append(LICENSE)
        builder.append('&sort=date-posted-desc')
        builder.append('&text=')
        
        encodedKeywords = urllib.quote(keywords.encode('utf-8'))
        builder.append(encodedKeywords)
        
        url = ''.join(builder)
        return url
        
        
        
    def get_image_url(self):
        builder = []
        builder.append('http://farm')
        builder.append(self.farm)
        builder.append('.static.flickr.com/')
        builder.append(self.server)
        builder.append('/')
        builder.append(self.id)
        builder.append('_')
        builder.append(self.secret)
        builder.append('_m.jpg')
        
        url = ''.join(builder)
        return url
        
        
        
    def get_page_url(self):
        builder = []
        builder.append('http://www.flickr.com/')
        builder.append(self.owner)
        builder.append('/')
        builder.append(self.id)
        
        url = ''.join(builder)
        return url
