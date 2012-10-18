# -*- coding: utf-8 -*-
from google.appengine.ext import db

from picture import Picture

class PictureHelper(object):
    # 最新の絵をデータストアから取得する
    def get_current_picture(self):
        q = db.Query(Picture)
        q.filter('isCurrent =', True)
        q.order('-createDate')
        result = q.get()

        return result

    # 最新の絵(存在すれば、複数枚)をデータストアから取得する
    def get_current_pictures(self):
        # 取得する数が不定なので、rpcオブジェクトを使用する
        # See: https://developers.google.com/appengine/docs/python/datastore/queryclass?hl=ja#Query_fetch
        rpc = db.create_rpc(deadline=10, read_policy=db.EVENTUAL_CONSISTENCY)
        return Picture.all().run(rpc=rpc)


    # 絵の作者の一人として登録する
    def connect_picture(self, clientId):
        # 最新の絵を取得する
        picture = self.get_current_picture()
        if picture == None:
            # 絵がない場合は、新たな絵を登録する
            clientIds = []
            clientIds.append(clientId)
            picture = Picture(
                              clientIds=clientIds,
                              isCurrent=True,
                              )
        else:
            picture.clientIds.append(clientId)

        picture.put()


    # 最新の絵に、描画情報を追加する
    def add_stroke(self, stroke):
        picture = self.get_current_picture()

        # 絵がない場合は、Noneを返す
        if picture == None:
            return None

        # strokeをそのまま入れると、[]で囲んであるためにリストと解釈されてしまうことから、
        # 明確にunicodeであることを示してあげる
        picture.strokes.append(db.Text(unicode(stroke)))
        picture.put()
        return picture


    # 現在の絵を取得する
    def get_picture(self):
        return self.get_current_picture()


    # 指定された絵を取得する
    # Javaはオーバーロードだったが、Pythonにはないので、メソッド名を変更した
    def get_picture_by_id(self, id):
        return Picture.get_by_id(int(id))


    # 新しい絵を作成する
    def create_new_picture(self):
        # 複数枚あるかもしれないため、picture"s" のメソッドを使う
        pictures = self.get_current_pictures()

        retpicture = None
        for picture in pictures:
            if len(picture.strokes) == 0:
                # 何も描かれていない場合は、削除する
                picture.delete()

            else:
                # 何か描かれている絵は、保存する
                picture.isCurrent = False
                picture.put()
                retpicture = picture

        return retpicture


    # 保存された絵をデータストアから取得する
    def get_history_pictures(self):
        q = db.Query(Picture)
        q.filter('isCurrent =', False)
        q.order('-createDate')
        result = q.fetch(20)

        return result


    # 保存された絵を返す
    def get_histories(self):
        return self.get_history_pictures()

