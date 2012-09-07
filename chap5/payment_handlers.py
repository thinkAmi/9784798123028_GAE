# -*- coding: utf-8 -*-

import webapp2
import os
import urlparse     # Python2.7なので、cgiではなくurlparseを使う
from google.appengine.ext.webapp import template

from paypal.helper import ExpressCheckout as EC
from paypal.souvenir import Souvenir
from paypal.error_operation import ErrorOperation



URL_START = '/paypal/'
URL_PAYMENT = '/paypal/payment'
URL_CANCEL_REDIRECT = '/paypal/redirect/cancel'
URL_CANCEL = '/paypal/cancel/'


class CartPageHandler(webapp2.RequestHandler):
    def get(self):
        souvenirInfo = Souvenir.get_souvenir()
    
        self.response.out.write(template.render('html/cart.html',
                                                {'name': souvenirInfo['name'],
                                                 'unitPrice': souvenirInfo['unitPrice'],
                                                }))
        
        
    def post(self):
        quantity = int(self.request.get('quantity'))
        
        souvenirInfo = Souvenir.get_souvenir()
        amount = (souvenirInfo['unitPrice'] + souvenirInfo['tax']) * quantity + souvenirInfo['carriage']
        
        nvpParams = {# APIの設定
                     'RETURNURL': self.request.host_url + URL_PAYMENT,
                     'CANCELURL': self.request.host_url + URL_CANCEL_REDIRECT,
                     'LANDINGPAGE': 'Billing',
                     'SOLUTIONTYPE': 'Sole',
                     'GIFTMESSAGEENABLE': 0,
                     'GIFTRECEIPTENABLE': 0,
                     'GIFTWRAPENABLE': 0,
                     'LOCALECODE': 'jp_JP',
                     'LANDINGPAGE': 'Billing',
                     'ALLOWNOTE': 0,
                     
                     # 商品全体の設定
                     'PAYMENTREQUEST_0_AMT': (souvenirInfo['unitPrice'] + souvenirInfo['tax']) * quantity + souvenirInfo['carriage'],
                     'PAYMENTREQUEST_0_CURRENCYCODE': souvenirInfo['currency'],
                     'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
                     'PAYMENTREQUEST_0_ITEMAMT': souvenirInfo['unitPrice'] * quantity,
                     'PAYMENTREQUEST_0_SHIPPINGAMT': souvenirInfo['carriage'],
                     'PAYMENTREQUEST_0_TAXAMT': souvenirInfo['tax'] * quantity,
                     
                     # 商品明細の設定
                     'L_PAYMENTREQUEST_0_ITEMCATEGORY0': 'Physical',
                     'L_PAYMENTREQUEST_0_NAME0': souvenirInfo['name'],
                     'L_PAYMENTREQUEST_0_QTY0': quantity,
                     'L_PAYMENTREQUEST_0_TAXAMT0': souvenirInfo['tax'],
                     'L_PAYMENTREQUEST_0_AMT0': souvenirInfo['unitPrice'],
                    }
        
        paypalResponse = EC.set_express_checkout(nvpParams)


        hasError = ErrorOperation.has_set_error(self.response, paypalResponse, 'SetExpressCheckout')
        if hasError:
            return
        
        contents = urlparse.parse_qs(paypalResponse.content)
        
        
        # tokenをつけて、PayPalのページへ移動
        redirect_url = EC.generate_express_checkout_redirect_url(contents['TOKEN'][0])
        return self.redirect(redirect_url)
        
        
        
class PaymentPageHandler(webapp2.RequestHandler):
    def get(self):
        paypalResponse = EC.get_express_checkout_details(self.request.get('token'))
        

        hasError = ErrorOperation.has_get_error(self.response, paypalResponse, 'GetExpressCheckoutDetails')
        if hasError:
            return


        contents = urlparse.parse_qs(paypalResponse.content)
        
        params = { # システムまわり
                           'postUrl': URL_PAYMENT + '?' + self.request.query_string,
                           
                           # 顧客情報
                           'email': contents['EMAIL'][0],
                           'firstname': contents['FIRSTNAME'][0],
                           'lastname': contents['LASTNAME'][0],
                           'shipToName': contents['PAYMENTREQUEST_0_SHIPTONAME'][0], # 姓名が入る
                           'shipToStreet': contents['PAYMENTREQUEST_0_SHIPTOSTREET'][0],
                           'shipToStreet2': contents['PAYMENTREQUEST_0_SHIPTOSTREET2'][0] if 'PAYMENTREQUEST_0_SHIPTOSTREET2' in contents else '',
                           'shipToCity': contents['PAYMENTREQUEST_0_SHIPTOCITY'][0],
                           'shipToState': contents['PAYMENTREQUEST_0_SHIPTOSTATE'][0],
                           'shipToZip': contents['PAYMENTREQUEST_0_SHIPTOZIP'][0],
                           # 日本では取得できない？
                           'shipToPhoneNo': contents['PAYMENTREQUEST_0_SHIPTOPHONENUM'][0] if 'PAYMENTREQUEST_0_SHIPTOPHONENUM' in contents else '',
                           
                           # 商品情報
                           'amount': contents['PAYMENTREQUEST_0_AMT'][0],
                           'itemAmount': contents['PAYMENTREQUEST_0_ITEMAMT'][0],
                           'shippingAmount': contents['PAYMENTREQUEST_0_SHIPPINGAMT'][0],
                           'taxAmount': contents['PAYMENTREQUEST_0_TAXAMT'][0],
                           'itemName': contents['L_PAYMENTREQUEST_0_NAME0'][0],
                           'itemUnitPrice': contents['L_PAYMENTREQUEST_0_AMT0'][0],
                           'quantity': contents['L_PAYMENTREQUEST_0_QTY0'][0],
                           'tax': contents['L_PAYMENTREQUEST_0_TAXAMT0'][0],
                           
                           # トランザクション情報：この時点では取得できない
                           #'transactionId': contents['PAYMENTREQUEST_0_TRANSACTIONID'][0],
                           #'requestId': contents['PAYMENTREQUEST_0_PAYMENTREQUESTID'][0],
                         }

        self.response.out.write(template.render('html/confirm.html',{'params': params,}))
        
        
    # 本ではgetしていたが、重要なデータがあるので同じクラスのpostに変更する
    # 本でgetしていた理由がわからない (hrefで次の画面に遷移していたため、postが使えない？)
    def post(self):
        payerId = self.request.get('PayerID')
        souvenirInfo = Souvenir.get_souvenir()
        
        
        # もう一度 GetExpressCheckoutで支払額合計を取得する
        paypalResponse = EC.get_express_checkout_details(self.request.get('token'))
        hasGetError = ErrorOperation.has_get_error(self.response, paypalResponse, 'GetExpressCheckoutDetails')
        if hasGetError:
            return
            
        contents = urlparse.parse_qs(paypalResponse.content)
            
        # get時と金額を変えてもエラーも何も出ずに決済されるので、そこが怖い...
        nvpParams = { 'PAYERID': payerId,
                      'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
                      'PAYMENTREQUEST_0_AMT': contents['PAYMENTREQUEST_0_AMT'][0],
                      'PAYMENTREQUEST_0_CURRENCYCODE': souvenirInfo['currency'],
                     }
        
        paypalResponse = EC.do_express_checkout_payment(self.request.get('token'),
                                                        nvpParams
                                                       )
        

        hasDoError = ErrorOperation.has_do_error(self.response, paypalResponse, 'DoExpressCheckoutPayment')
        if hasDoError:
            return
        

        self.response.out.write(template.render('html/success.html',{}))
        
        

class CancelHandler(webapp2.RequestHandler):
    def get(self):
        # URLにtokenがついてやってくるため、キャンセルページヘリダイレクト
        return self.redirect(self.request.host_url + URL_CANCEL)

        
class CancelPageHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render('html/cancel.html',{}))


            
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

app = webapp2.WSGIApplication([(URL_START, CartPageHandler),
                               (URL_PAYMENT + '*', PaymentPageHandler),
                               (URL_CANCEL_REDIRECT + '.*', CancelHandler),
                               (URL_CANCEL, CancelPageHandler),
                              ],
                              debug=debug)
