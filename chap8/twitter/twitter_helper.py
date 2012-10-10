# -*- coding: utf-8 -*-

import logging
import python_twitter.twitter as twitter

import api_config

class TwitterHelper(object):
    
    # アクセストークンで認可されたTwitterオブジェクトを取得する
    @staticmethod
    def get_twitter():
        return twitter.Api(consumer_key=api_config.Twitter.CONSUMER_KEY,
                           consumer_secret=api_config.Twitter.CONSUMER_SECRET,
                           access_token_key=api_config.Twitter.ACCESS_TOKEN_KEY,
                           access_token_secret=api_config.Twitter.ACCESS_TOKEN_SECRET,
                           cache=None       # GAEなので、キャッシュは使わない
                           )


    # タイムラインにツイートを投稿する
    @classmethod
    def tweet(self, status):
        api = self.get_twitter()
        api.PostUpdate(status)


    # フォロー返しをする
    @classmethod
    def refollow(self):
        api = self.get_twitter()
        # フォローアカウントの一覧を取得し、set型にしておく
        friends = set(api.GetFriends())
        # フォロワーアカウントの一覧を取得し、set型にしておく
        followers = set(api.GetFollowers())

        # フォローしていない人を取得し、フォローする
        nonFriends = followers.difference(friends)
        for nonFriend in nonFriends:
            try:
                api.CreateFriendship(nonFriend.id)
            except:
                # フォローできない人がいても、警告ログを出して処理は続行する
                logging.info('Cannot follow:' + nonFriend.screen_name)


    # リムーブする
    @classmethod
    def remove(self):
        api = self.get_twitter()
        # フォローアカウントの一覧を取得し、set型にしておく
        friends = set(api.GetFriends())
        # フォロワーアカウントの一覧を取得し、set型にしておく
        followers = set(api.GetFollowers())

        # フォロワーアカウントにいない人を取得し、リムーブする
        nonFollowers = friends.difference(followers)
        for nonFollower in nonFollowers:
            try:
                api.DestroyFriendship(nonFollower.id)
            except:
                # フォローを外せない人がいても、警告ログを出して処理は続行する
                logging.info('Cannot remove:' + nonFollower.screen_name)


    # フォロワーのタイムラインを取得する
    @classmethod
    def get_follower_timeline(self):
        api = self.get_twitter()
        return api.GetFriendsTimeline()

    # ぐぐるちゃんのUserインスタンスを取得する
    @classmethod
    def get_guguruchan(self):
        api = self.get_twitter()
        return api.VerifyCredentials()
