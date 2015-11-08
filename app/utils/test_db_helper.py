#! -*- coding:utf8 -*-

from db_helper import DB42
from tornado import gen
import tornado.ioloop

ioloop = tornado.ioloop.IOLoop.instance()
db = DB42('127.0.0.1', 3306, 'root', 'qweasd', 'test', 8)

@gen.engine
def test_do_query():
    result, error = yield db.query("select * from test_user", None)
    print result, error
@gen.engine
def test_do_update():
    result, error = yield db.update("insert into test_user(id, name, create_time) values(%s, %s, now())", [2, 'peter'])
    print result, error

if '__main__' == __name__:
    ioloop.add_callback(test_do_update)
    ioloop.add_callback(test_do_query)
    ioloop.start()
