#! -*- coding:utf8 -*-
# user model
#
import sys
import json
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
		return str(json.loads(self._data)['name'])

	def description(self):
		return str(json.loads(self._data)['desc'])
	def to_json(self):
		user_of_json = self.__dict__
		user_of_json['_create_time'] = str(user_of_json['_create_time'])
		return user_of_json

class UserDAO(object):
	def __init__(self):
		self._db = DB42('127.0.0.1', 3306, 'root', 'qweasd', 'user')

	def GetByIds(self, ids):
		SQL = "select * from user where id in (" + ",".join(map(str,ids)) + ")"
 		result = self._db.query(SQL)
		print result
		# TODO (1L, u'mary', u'{}', 0L, datetime.datetime(2015, 11, 8, 15, 49, 33)) to Users
		users = []
		if result[0]:
			for eachItem in result[1]:
				users.append(User(eachItem[0], eachItem[1], eachItem[2], eachItem[3], eachItem[4]))
		else:
			users.append(User(result[1][0], result[1][1], result[1][2], result[1][3], result[1][4]))
		return users

	def InsertOrUpdate(self, username, data, status):
		params = [username, data, status]
		result = self._db.update("insert into user(username, data, status, create_time) values(%s, %s, %s, now())", params)
		print result
		return result
