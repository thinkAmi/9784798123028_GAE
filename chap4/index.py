# -*- coding: utf-8 -*-

import webapp2
import datetime
import os
from google.appengine.ext.webapp import template

import alarm
import gae_util

class IndexPage(webapp2.RequestHandler):
    def get(self):
        
        utcnow = datetime.datetime.utcnow()
        jstTime = gae_util.Utility.convert_jst_time(utcnow)
        
        if jstTime.hour >= 7:
            jstTime = jstTime + datetime.timedelta(days=1)

        self.response.out.write(template.render('html/index.html',{'selectedYear': jstTime.year,
                                                                   'selectedMonth': jstTime.month,
                                                                   'selectedDate': jstTime.day,
                                                                   'selectedHourOfDay': 7,
                                                                   'selectedMinute': 0,
                                                                   'years': self.get_years(),
                                                                   'months': self.get_months(),
                                                                   'dates': self.get_dates(),
                                                                   'hours': self.get_hours(),
                                                                   'minutes': self.get_minutes(),
                                                                   }))
        
        
    def post(self):
        
        email = self.request.get("email")
        nickname = self.request.get("nickname")
        year = self.request.get("year")
        month = self.request.get("month")
        date = self.request.get("date")
        hourOfDay = self.request.get("hourOfDay")
        minute = self.request.get("minute")
        
        
        # 入力チェック
        hasError = False
        emailError = False
        nicknameError = False
        wakeupDateError = False
        
        if email is None or email== '':
            emailError = True
            hasError = True
            
        if nickname is None or nickname == '':
            nicknameError = True
            hasError = True
            
        if not self.is_datetime(year, month, date):
            wakeupDateError = True
            hasError = True
        
        
        if hasError:
            # テンプレートの ifequal で正しく出力するには型を揃える必要があるため、int型へと変換しておく
            self.response.out.write(template.render('html/index.html',{'selectedYear': int(year),
                                                                       'selectedMonth': int(month),
                                                                       'selectedDate': int(date),
                                                                       'selectedHourOfDay': int(hourOfDay),
                                                                       'selectedMinute': int(minute),
                                                                       'years': self.get_years(),
                                                                       'months': self.get_months(),
                                                                       'dates': self.get_dates(),
                                                                       'hours': self.get_hours(),
                                                                       'minutes': self.get_minutes(),
                                                                       'email': email,
                                                                       'emailError': emailError,
                                                                       'nickname': nickname,
                                                                       'nicknameError': nicknameError,
                                                                       'wakeupDateError': wakeupDateError,
                                                                       }))
            return
              
        
        
        # データストアへの登録
        wakeupDate = datetime.datetime(int(year), int(month), int(date), int(hourOfDay), int(minute))
        
        #データストアの時刻は、タイムゾーンを考慮しないUTC時刻のため、タイムゾーンを加味して設定する
        jstWakeupDate = gae_util.Utility.convert_jst_time(wakeupDate)
        
        datastore = alarm.Alarm(key_name = email,
                      email = email,
                      nickname = nickname,
                      wakeupDate = jstWakeupDate,
                      count = 0)
        datastore.put()
        
        self.response.out.write(template.render('html/index_post.html',{'email': email,
                                                                        'nickname': nickname,
                                                                        'wakeupDate': wakeupDate,
                                                                        }))

    def get_years(self):
        #年は2年分
        utcnow = datetime.datetime.utcnow()
        years = []
        years.append(utcnow.year)
        years.append(utcnow.year + 1)
        
        return years
        
        
    def get_months(self):
        months = []
        
        for month in range(1, 13):
            months.append(month)
        
        return months
        
        
    def get_dates(self):
        dates = []
        
        for date in range(1, 32):
            dates.append(date)
            
        return dates
        
        
    def get_hours(self):
        hours = []
        
        for hour in range(0, 24):
            hours.append(hour)
        
        return hours
        
            
    def get_minutes(self):
        minutes = []
        
        for minute in range(0, 59, 5):
            minutes.append(minute)
            
        return minutes
    
    
    def is_datetime(self, year, month, date):
        try:
            datetime.date(int(year), int(month), int(date))
            return True
            
        except ValueError:
            return False
            
            
            
            
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
            
app = webapp2.WSGIApplication([('/index.html', IndexPage),
                               ('/', IndexPage)], debug=debug)
