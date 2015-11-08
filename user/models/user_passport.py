#! -*- coding:utf8 -*-
# 登陆信息
import json
from datetime import datetime
import sys
sys.path.append("..")
from base.db_helper import DB42

class UserPassport(object):
    def __init__(self, id, account, password, status, update_time, create_time):
        self._id = id # userId
        self._account = account
        self._password = password
        self._status = status
        self._update_time = update_time
        self._create_time = create_time

class PassportDAO(object):
    def __init__(self):
        self._db = DB42('127.0.0.1', 3306, 'root', 'qweasd', 'user', 8)
    def  GetByAccountPassword(self, account, password):
        params = [account, password]
        # TODO deal with callback way
        result = self._db.query("select * from user_passport where account = %s and password = %s", params)
        # TODO transfer (1L, u'mary', u'123asd', 0L, 20151108032450L, datetime.datetime(2015, 11, 8, 3, 24, 50)) to model
        if result[1]:
            return UserPassport(result[1][0],result[1][1],result[1][2],result[1][3],result[1][4],result[1][5])

    def InsertOrUpdate(self, account, password, status):
        params = [username, data, status]
        result = self._db.update("insert into user_passport(account, password, status, update_time, create_time) values(%s, %s, %s, now(), now())", params)
        print result
        return result
