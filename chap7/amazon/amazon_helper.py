# -*- coding: utf-8 -*-

from lxml import objectify
import datetime
from google.appengine.api import memcache

import fresh_pub
from bottlenose.api import Amazon
import amazon.amazon_config as amazonConfig


class AmazonHelper(object):

    # 新刊情報を返す
    def get_fresh_pubs(self, title, author, publisher):

        amazon = Amazon(
                amazonConfig.AWS_KEY, 
                amazonConfig.SECRET_KEY, 
                amazonConfig.ASSOCIATE_TAG, 
                Region='JP'
                )


        freshPubs = []
        maxResults = 40     # 最大40件の表示
        itemPage = 0

        while len(freshPubs) < maxResults:

            # 少し待つ
            self._wait_access()

            # 何件目から検索するかを指定して、APIをbottlenose経由で呼び出す
            itemPage += 1
            response = self._search(amazon, title, author, publisher, itemPage)


            # 新刊情報オブジェクトを検索結果に追加する
            pubs = self._create_fresh_pub(response)
            freshPubs.extend(pubs)


            # 最大件数の調整
            if itemPage == 1:
                totalResults = self._get_total_results(response)
                maxResults = maxResults if maxResults < totalResults else totalResults

                if len(freshPubs) >= maxResults:
                    break

        return freshPubs



    # アプリ全体を通して、処理が一秒以上の間隔で行われるようにする
    def _wait_access(self):
        while True:
            lastAccess = memcache.get('lastDate')
            if lastAccess == None:
                lastAccess = datetime.datetime(1970,1,1)

            current = datetime.datetime.utcnow()
            if lastAccess + datetime.timedelta(seconds=1) < current:
                memcache.set('lastDate', current)
                return

            try:
                time.sleep(1)
            except:
                pass



    # Amazonからbottlenose経由でデータを取得する
    def _search(self, amazon, title, author, publisher, itemPage):

        return amazon.ItemSearch(
                                 SearchIndex='Books',
                                 Sort='daterank',
                                 ItemPage=itemPage,
                                 ResponseGroup='ItemAttributes, Offers',
                                 Condition='All',
                                 Title=title,
                                 Author=author,
                                 Publisher=publisher
                                )


    # Amazonの検索結果から、「タイトル」「書籍URL」「刊行日」を取得して、新刊情報オブジェクトを生成
    def _create_fresh_pub(self, response):
        pubs = []

        root = objectify.fromstring(response)
        for item in root.Items.Item:
            pub = fresh_pub.FreshPub(
                                     item.ItemAttributes.Title,
                                     unicode(item.Offers.MoreOffersUrl),
                                     item.ItemAttributes.PublicationDate
                                    )
            pubs.append(pub)

        return pubs


    # Amazonの検索結果から、総検索結果数を取得する
    def _get_total_results(self, response):
        root = objectify.fromstring(response)

        for item in root.Items:
            return item.TotalResults
