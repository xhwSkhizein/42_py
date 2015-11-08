#! -*- coding:utf8 -*-
# user model
#
import sys
sys.path.append("../..")
from utils.db_helper import DB42

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

class UserDAO(object):
	global _db
	_db = DB42('127.0.0.1', 3306, 'root', 'qweasd', 'user')
	def GetByIds(self, ids):
		def get_by_ids(self, ids):
	 		result = _db.query("select * from user where id in (%s)", ids)
			print result
			return result
		return get_by_ids(ids)

	def InsertOrUpdate(self, username, data, status):
		params = [username, data, status]
		def insert_or_update(self, username, data, status):
			result = _db.update("insert into user(username, data, status, create_time) values(%s, %s, %s, now())", params)
			print result
			return result
		return insert_or_update(*params)
