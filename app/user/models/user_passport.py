#! -*- coding:utf8 -*-
# 登陆信息

from utils.db_helper import DB42
from tornado import gen
from constant.db_constants import DB_Name_Of_
import tornado.ioloop

class UserPassport(object):
    def __init__(self, id, account, password, status, update_time, create_time):
        self._id = id # userId
        self._account = account
        self._password = password
        self._status = status
        self._update_time = update_time
        self._create_time = create_time

_db = DB42('127.0.0.1', 3306, 'root', 'qweasd', DB_Name_Of_.user, 8)
_ioloop = tornado.ioloop.IOLoop.instance()

class PassportDAO(object):
    def  ByAccountPassword(account, password):
        params = [account, password]
        @gen.engine
        def get_by_account_password():
            result, error = yield _db.query("select * from user_passport where account = %s and password = %s", params)
            print result, error
            return result if result else raise error
        _ioloop.add_callback(get_by_account_password)

    def InsertOrUpdate(account, password, status):
        params = [username, data, status]
        @gen.engine
        def insert_or_update(account, password, status):
            result, error = yield _db.update("insert into user_passport(account, password, status, update_time, create_time) values(%s, %s, %s, now(), now())", params)
            print result, error
            return result if result else raise error
        _ioloop.add_callback(insert_or_update)
