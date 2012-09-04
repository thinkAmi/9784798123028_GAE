# -*- coding: utf-8 -*-

import datetime
from google.appengine.ext import db

import blogs
import flickr.flickr_helper
import gae_util


def get_avatar_instances():
    return [ EriAvatar(), SounAvatar(), O2Avatar()]


class Avatar(object):

    # プロパティ関連
    def __init__(self):
        self._id = ''
        self._name = ''
        self._imageName = ''
        self._message = ''
        
    @property
    def id(self):
        return self._id
        
    @id.setter
    def id(self, values):
        self._id = values
        
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, values):
        self._name = values


    @property
    def imageName(self):
        return self._imageName
        
    @imageName.setter
    def imageName(self, values):
        self._imageName = values
        
        
    @property
    def message(self):
        return self._message
        
    @message.setter
    def message(self, values):
        self._message = values
        


    # スタティックメソッド関連
    @staticmethod
    def get_avatar(avatarId):
        instances = get_avatar_instances()
        for instance in instances:
            if instance.id == avatarId:
                return instance

    @staticmethod
    def get_avatars():
        return get_avatar_instances()


    # オーバーライドメソッド
    def create_article(self, blog):
        pass


    # 継承メソッド群
    def add_article(self, blog, text, keywords, nextPostTime):
    
        helper = flickr.flickr_helper.FlickrHelper()
        helper.fetch(keywords)
        
        
        pageUrl = ''
        imageUrl = ''
        
        if helper.id != '':
            pageUrl = helper.get_page_url()
            imageUrl = helper.get_image_url()
            
            
        
        # run_in_transaction_optionsによるトランザクション
        params = {'blogId': blog.id,
                  'text': text,
                  'nextPostTime': nextPostTime,
                  'pageUrl': pageUrl,
                  'imageUrl': imageUrl
                 }
        
        
        # ★以下のニ行をアンコメントすることで、トランザクションを使わなくなる★
        #self.run_xg_transaction(params)
        #return
        
        xg_options = db.create_transaction_options(xg=True, retries=3)
        db.run_in_transaction_options(xg_options,
                                      self.run_xg_transaction,
                                      params)
            

    def run_xg_transaction(self, params):
        jstnow = gae_util.Utility.get_jst_now()
        
        blogId = params['blogId']
        blog = blogs.Blog.get_by_key_name(str(params['blogId']))

        # 親ブログの更新
        nextPostTime = params['nextPostTime']
        if nextPostTime >= 0:
            # 本では時間を加算していたが、時間短縮のため分を加算する
            blog.nextPostDate = jstnow + datetime.timedelta(minutes=nextPostTime)
            blog.articleCount += 1

        else:
            blog.nextPostDate = datetime.datetime(9999,12,31,0,0,0)
            
        blog.put()
        
        
        # ★強制的に例外を起こすためには、以下の一行をアンコメント★
        #raise ValueError("*-------Error--------*")
        

        # 記事の登録
        article = blogs.Article(id = jstnow,
                                blog = blog,
                                postDate = jstnow,
                                text = params['text'],
                                pageUrl = params['pageUrl'],
                                imageUrl = params['imageUrl'],
                                )
                                
        article.put()
    
    
    def abort_blog(self, blog):
        blog.nextPostDate
        blog.put()
        



class EriAvatar(Avatar):

    # プロパティにセット
    def __init__(self):
        super(Avatar, self).__init__()
        self.id = u'eri'
        self.name = u'えり'
        self.imageName = u'avatar_eri.jpg'
        self.message = u'それじゃあ、いってきます。感動したことがあったらblogに書くので、見てね。'
    

    def create_article(self, blog):
        if blog.articleCount == 0:
            self.add_article(blog,
                             u'思ったより遠くてちょっと疲れた。明日からは' + blog.destination + u'をいろいろと見て回ろう。今日はお休み。',
                             blog.destination,
                             5)
                             
        elif blog.articleCount == 1:
            self.add_article(blog,
                             u'ここに来る前からグルメ雑誌で調べていた料理を食べたよ。もー、ほんとおいしかった。',
                             blog.destination + u' meal',
                             5)
                             
        elif blog.articleCount == 2:
            self.add_article(blog,
                             blog.destination + u'の名所にやってきた。写真と本物では、大違いだなぁ。来てよかった。',
                             blog.destination + u' famous',
                             5)
                             
        elif blog.articleCount == 3:
            self.add_article(blog,
                             blog.destination + u'の旅、本当に楽しかった。来年もまた来よう。',
                             blog.destination + u' evening',
                             -1)
                             
        else:
            self.abort_blog(blog)
            
            
            
class SounAvatar(Avatar):

    # プロパティにセット
    def __init__(self):
        super(Avatar, self).__init__()
        self.id =  u'soun'
        self.name = u'早雲'
        self.imageName = u'avatar_soun.jpg'
        self.message = u'じゃあ、いってくる。何が待っているか楽しみだ。見て聞いて感じたことをblogに書くので、読んでくれよな。'


    def create_article(self, blog):
        if blog.articleCount == 0:
            self.add_article(blog,
                             blog.destination + u'に到着！　今日はとりあえず寝る。明日からは' + blog.destination + u'巡り、がんばるぞ！',
                             blog.destination,
                             5)
                             
        elif blog.articleCount == 1:
            self.add_article(blog,
                             blog.destination + u'はまるで、時の流れが止まったかのようだ。なにもかもが美しい。',
                             blog.destination + u' time',
                             5)
                             
        elif blog.articleCount == 2:
            self.add_article(blog,
                             u'旅も明日で終わりだ。みんなにいろいろ土産を買おうと思って探したら、これを見つけた。どうだろう？',
                             blog.destination + u' souvenir',
                             5)
                             
        elif blog.articleCount == 3:
            self.add_article(blog,
                             u'今回の旅は、僕には忘れられない体験となった。いつかまた' + blog.destination + u'を訪れたい。',
                             blog.destination + u' scene',
                             -1)
                             
        else:
            self.abort_blog(blog)



class O2Avatar(Avatar):

    # プロパティにセット
    def __init__(self):
        super(Avatar, self).__init__()
        self.id = u"o2"
        self.name = u"O2"
        self.imageName = u"avatar_o2.jpg"
        self.message = u'ホイジャア、行ッテクルガネ。気ガ向イタラblogヲ書クンデ、読ヨンデチョ。'


    def create_article(self, blog):
        if blog.articleCount == 0:
            self.add_article(blog,
                             u'夢ニマデミタ' + blog.destination + u'ニ着イチマッタダガネ。ヨーケ休ンデ明日カラウロウロシヨマイ。',
                             blog.destination,
                             5)
                             
        elif blog.articleCount == 1:
            self.add_article(blog,
                             u'見タコトモナイ鳥ガオッタ。ヤッパ' + blog.destination + u'ハ、チャウナア',
                             blog.destination + u' bird',
                             5)
                             
        elif blog.articleCount == 2:
            self.add_article(blog,
                             u'オ菓子ヲ買ッタ。ろぼっとダケド。',
                             blog.destination + u' goody',
                             5)
                             
        elif blog.articleCount == 3:
            self.add_article(blog,
                             u'ソロソロばってりガ無クナリソウダ。早ヨ帰ッテ充電シヨマイ。',
                             blog.destination + u' road',
                             -1)
                             
        else:
            self.abort_blog(blog)
