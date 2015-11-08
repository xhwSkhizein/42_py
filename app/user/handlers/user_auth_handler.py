#! -*- coding:utf8 -*-

import tornado.web
# import user_passport.PassportDAO
#from user.models.user import UserDAO
import tornado.ioloop
from tornado import gen
from db_helper import DB42

class AuthHandler(tornado.web.RequestHandler):
    '''
    # 登陆验证的handler
    # 验证成功     : 返回票和用户信息
    # 验证失败     : 返回 401 error_code
    # Router      : r"/user/auth" POST
    # ParamField  : account, password
    '''
    def post(self):
        account = self.get_body_argument("account")
        password = self.get_body_argument("password")
        t = authenticate(account, password)
        self.write(t);

    @gen.coroutine
    def get(self):
        account = self.get_query_argument("account")
        password = self.get_query_argument("password")
        # t = authenticate(account, password)
        #def authenticate(account, password):
        result = PassportDAO().ByAccountPassword(account, password)
        print("****" + str(result))
        # return result
        self.write(result)

class PassportDAO(object):
    def __init__(self):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self._db = DB42('127.0.0.1', 3306, 'root', 'qweasd', 'user', 8)

    def  ByAccountPassword(self, account, password):
        params = [account, password]
        @gen.coroutine
        def get_by_account_password():
            result, error = yield self._db.query("select * from user_passport where account = %s and password = %s", params)
            def callback(res):
                print("***&&&" + str(res))
            print("***&&&" + str(result))
            # result.add_done_callback(callback)
            # raise gen.Return(result)
            return str(result)
        self.ioloop.add_callback(get_by_account_password)

    def InsertOrUpdate(self, account, password, status):
        params = [username, data, status]
        @gen.coroutine
        def insert_or_update(account, password, status):
            result, error = yield self._db.update("insert into user_passport(account, password, status, update_time, create_time) values(%s, %s, %s, now(), now())", params)
            def callback(res):
                    print("***&&&" + str(res))
            print("***&&&" + str(result))
            # result.add_done_callback(callback)
            # raise gen.Return(result)
            return str(result)
        self.ioloop.add_callback(insert_or_update)


application = tornado.web.Application([
	(r"/user/auth", AuthHandler),
])

if __name__ == "__main__":
	application.listen(8081)
	tornado.ioloop.IOLoop.current().start()
