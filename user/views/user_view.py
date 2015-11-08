#! -*- coding:utf8 -*-
# user view
#
import sys
sys.path.append("..")
from base.entity_id_helper import EntityIdHelper


class UserView(object):

    def __init__(self, user_obj):
        # FIXME 抽出encode和decode部分
        self.id = EntityIdHelper().encode(user_obj._id, "User")
        self.username = user_obj.username_raw() if user_obj.username_raw() else user_obj._username
        self.createTime = str(user_obj._create_time)
        self.description = user_obj.description()

    def to_json(self):
        return self.__dict__
