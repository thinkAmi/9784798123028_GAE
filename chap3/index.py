# -*- coding: utf-8 -*-

from google.appengine.api import xmpp
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import bots


class XMPPHandler(webapp2.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        
        fromMe = message.sender
        toBot = message.to
        
        bot = bots.Bot.get_bot(toBot.split('@')[0])
        haiku = bot.make_haiku()
        
        xmpp.send_message(fromMe, haiku)
        
        
app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)], debug=True)