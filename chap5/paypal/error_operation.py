# -*- coding: utf-8 -*-
import urlparse     # Python2.7なので、cgiではなくurlparseを使う
import logging

from google.appengine.ext.webapp import template


class ErrorOperation:

    @classmethod
    def has_set_error(cls, webapp2Response, paypalResponse, apiName):
        return cls._has_unknown_error(webapp2Response, paypalResponse, apiName)
        
        
    @classmethod
    def has_get_error(cls, webapp2Response, paypalResponse, apiName):
        return cls._has_unknown_error(webapp2Response, paypalResponse, apiName)
        
        
    @classmethod
    def has_do_error(cls, webapp2Response, paypalResponse, apiName):
    
        if cls._has_unknown_error(webapp2Response, paypalResponse, apiName):
            return True
            
        return cls._has_unsucessful_error(webapp2Response, paypalResponse, apiName)
        
        

    # PayPal API でのunknownエラーが発生していないか？
    @classmethod
    def _has_unknown_error(cls, webapp2Response, paypalResponse, apiName):
    
        if paypalResponse.status_code != 200:
            cls._show_error_request(webapp2Response, paypalResponse.status_code, apiName)
            
            return True
            
        
        
        contents = urlparse.parse_qs(paypalResponse.content)
        
        if contents['ACK'][0] != 'Success':
            cls._show_error_contents(webapp2Response, contents, apiName)

            return  True
            
        
        # has_key()とinは同じ動きだが、Python3よりhas_key()が消えたので、inを採用
        # See: http://www.atmarkit.co.jp/fcoding/articles/python3/01/python301a.html
        if u'TOKEN' not in contents:
            cls._show_error_contents(webapp2Response, contents, apiName)
            
            return  True
            
            
            
        # 何もエラーがないとき
        return False
    
    
    
    # 支払処理が成功したか？
    @classmethod
    def _has_unsucessful_error(cls, webapp2Response, paypalResponse, apiName):

        contents = urlparse.parse_qs(paypalResponse.content)
        
        if u'PAYMENTINFO_0_PAYMENTSTATUS' not in contents:
            cls._show_error_contents(webapp2Response, contents, apiName)
            
            return True
            
        
        # おそらく eCheckの時に発生するエラー
        if contents['PAYMENTINFO_0_PAYMENTSTATUS'][0] != 'Completed':
            cls._show_error_contents(webapp2Response, contents, apiName)
            
            return True
    
    
        # 何もエラーがないとき
        return False
    
    
    # 【共通】エラーでのログ出力と画面の描画
    @staticmethod
    def _show_error_request(webapp2Response, paypalResponseStatusCode, apiName):
        logging.error(u'API Name: ' + apiName + u' and '
                      u'StatusCode: ' + paypalResponseStatusCode)
                          
        webapp2Response.out.write(template.render('html/payment_error.html',{}))
    
    
    @staticmethod
    def _show_error_contents(webapp2Response, contents, apiName):
        logging.error(u'API Name: ' + apiName)
        logging.error(contents)
            
        webapp2Response.out.write(template.render('html/payment_error.html',{}))
    