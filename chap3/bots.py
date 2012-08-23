# -*- coding: utf-8 -*-


#class Bot():
class Bot(object):
    def __init__(self):
        self._firstWords = []
        self._middleWords = []
        self._lastWords = []
        self._author = ''
        
    @property
    def firstWords(self):
        return self._firstWords
        
    @firstWords.setter
    def firstWords(self, values):
        self._firstWords = values
        
    
    @property
    def middleWords(self):
        return self._middleWords
        
    @middleWords.setter
    def middleWords(self, values):
        self._middleWords = values
    
        
    @property
    def lastWords(self):
        return self._lastWords
        
    @lastWords.setter
    def lastWords(self, values):
        self._lastWords = values


    @property
    def author(self):
        return self._author
        
    @author.setter
    def author(self, values):
        self._author = values



    @classmethod
    def get_bot(cls, botName):
        bots = {'eri': EriBot(),
                'soun': SounBot(),
                'o2': O2Bot()}
    
        return bots[botName]
    
    
    
    def make_haiku(self):
        haiku = self.choice(self.firstWords) + u'　' + self.choice(self.middleWords) + u'　' + self.choice(self.lastWords) + u'　'  + self.author
        return haiku
        
        
    def choice(self, words):
        import random
        
        randomIndex = random.randint(0, len(words) - 1)
        return words[randomIndex]
            
    
        
class EriBot(Bot):

    def __init__(self):
        super(Bot, self).__init__()
        self.firstWords = [u'淡雪や', u'向日葵や', u'名月や', u'クリスマス', u'初夢や']
        self.middleWords = [u'あなたのそばで', u'なじみのカフェで', u'ブランコに乗り', u'10年後にも', u'映画のように']
        self.lastWords = [u'見つめたい', u'手に取りたい', u'歌いたい', u'送りたい', u'眠りたい']
        self.author = '(Eri Bot)'
        
        
class SounBot(Bot):

    def __init__(self):
        super(Bot, self).__init__()
        self.firstWords = [u'簡単に', u'楽しげに', u'悲しげに', u'おおまかに', u'盛大に']
        self.middleWords = [u'旅先決める', u'小物を買うや', u'家路につきし', u'予定を立てる', u'友を祝いし']
        self.lastWords = [u'蜃気楼', u'五月晴れ', u'秋の空', u'除夜の鐘', u'年賀状']
        self.author = '(Soun Bot)'

        
class O2Bot(Bot):

    def __init__(self):
        super(Bot, self).__init__()
        self.firstWords = [u'気モ早ク', u'待チ切レズ', u'腹ガヘリ', u'俳句部デ', u'機械ナノニ']
        self.middleWords = [u'甘酒飲ミシ', u'ソウメン流シ', u'オ芋恋シヤ', u'鍋ヲツツキシ', u'豪華ナオセチダ']
        self.lastWords = [u'すかいつりー', u'名古屋城', u'西浦和', u'瀬戸内海', u'普賢岳']
        self.author = '(O2 Bot)'
