# -*- coding: utf-8 -*-

from google.appengine.api import users

# ログイン済であれば、リクエスト属性にユーザー情報を保存する
def do_filter():
    user = users.get_current_user()

    if user == None:
        return None, None

    if user.nickname():
        return user, user.nickname()

    if user.email():
        return user, user.email().split('@')[0]

    return user, user.user_id()





