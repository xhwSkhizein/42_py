#! -*- coding:utf8 -*-
# 登陆信息
import sys
sys.path.append("../..")
from utils.db_helper import DB42

class UserPassport(object):
    def __init__(self, id, account, password, status, update_time, create_time):
        self._id = id # userId
        self._account = account
        self._password = password
        self._status = status
        self._update_time = update_time
        self._create_time = create_time

class PassportDAO(object):
    global _db
    _db = DB42('127.0.0.1', 3306, 'root', 'qweasd', 'user', 8)
    def  GetByAccountPassword(self, account, password):
        params = [account, password]
        def get_by_account_password(params):
            result = _db.query("select * from user_passport where account = %s and password = %s", params)
            # TODO transfer (1L, u'mary', u'123asd', 0L, 20151108032450L, datetime.datetime(2015, 11, 8, 3, 24, 50)) to model
            up = UserPassport(result[0],result[1],result[2],result[3],result[4],result[5])
            return up
        return get_by_account_password(params)

    def InsertOrUpdate(self, account, password, status):
        params = [username, data, status]
        def insert_or_update(account, password, status):
            result = _db.update("insert into user_passport(account, password, status, update_time, create_time) values(%s, %s, %s, now(), now())", params)
            print result
            return result
        return insert_or_update(params)
