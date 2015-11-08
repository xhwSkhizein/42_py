#! -*- coding:utf8 -*-
# user view
#
import base64

class UserView(object):

    def __init__(self, user_obj):
        self.id = base64.b64encode(str(user_obj._id) + str(user_obj._create_time) + "salt")
        self.username = user_obj.username_raw() if user_obj.username_raw() else user_obj._username
        self.createTime = str(user_obj._create_time)
        self.description = user_obj.description()

    def to_json(self):
        return self.__dict__
