#! -*- coding:utf8 -*-
# 标准请求响应
#
import sys
sys.path.append("../user")
from models.user import User
from views.user_view import UserView
import datetime


class ResponseWrapper(object):
    def __init__(self, message = None, status=200):
        self.message = message
        self.status = status
        self.data = {}

    def add(self, key, value):
        self.data[key] = value
        return self

    def addAll(self, data):
        for k in data.keys():
            self.data[k] = data[k]
        return self

    def to_json(self):
        return self.__dict__


if __name__ == '__main__':
    r = ResponseWrapper()
    print r.__doc__
    print r.to_json()
    user = User(1L, u'mary', u'{"name":"Mary","desc":"Im Mary."}', 0L, datetime.datetime(2015, 11, 8, 15, 49, 33))
    userview = UserView(user)
    r.add("user", userview.to_json())
    print r.to_json()
