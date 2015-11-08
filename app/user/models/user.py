#! -*- coding:utf8 -*-
# user model
#
from utils.db_helper import DB42
from tornado import gen
from constant.db_constants import DB_Name_Of_
import tornado.ioloop

class User:
	def __init__(self, id, name, data, status, create_time):
		self._id = id
		self._username = name
		self._data = data
		self._status = status
		self._create_time = create_time

	def username_raw(self):
		return str(dict(self._data)['name'])
	def description(self):
		return str(dict(self._data)['desc'])

_db = DB42('127.0.0.1', 3306, 'root', 'qweasd', DB_Name_Of_.user, 8)
_ioloop = tornado.ioloop.IOLoop.instance()

class UserDAO(object):
	def ByIds(ids):
		params = ids
		@gen.engine
		def get_by_ids(self, ids):
			result, error = yield _db.query("select * from user where id in (%s)", ids)
			print result, error
			return result if result else raise error
		_ioloop.add_callback(get_by_ids)

	def InsertOrUpdate(username, data, status):
		params = [username, data, status]
		@gen.engine
		def insert_or_update(self, username, data, status):
			result, error = yield _db.update("insert into user(username, data, status, create_time) values(%s, %s, %s, now())", params)
			print result, error
			return result if result else raise error
		_ioloop.add_callback(insert_or_update)
