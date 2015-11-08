#! -*- coding:utf8 -*-

import tornado.web
#from user.models.user import UserDAO
import tornado.ioloop
import sys
sys.path.append("..")
from utils.db_helper import DB42
from user_passport import PassportDAO

class AuthHandler(tornado.web.RequestHandler):
    '''
    # 登陆验证的handler
    # 验证成功     : 返回票和用户信息
    # 验证失败     : 返回 401 error_code
    # Router      : r"/user/auth" POST
    # ParamField  : account, password
    '''
    # def post(self):
    #     account = self.get_body_argument("account")
    #     password = self.get_body_argument("password")
    #     t = authenticate(account, password)
    #     self.write(t);

    def get(self):
        account = self.get_query_argument("account")
        password = self.get_query_argument("password")
        # t = authenticate(account, password)
        #def authenticate(account, password):
        user_passport = PassportDAO().GetByAccountPassword(account, password)
        if user_passport:
            # TODO get user info and return json format result
            self.write(str(user_passport._id))
        else:
            self.write("401, authentication failure!")



application = tornado.web.Application([
	(r"/user/auth", AuthHandler),
])

if __name__ == "__main__":
	application.listen(8081)
	tornado.ioloop.IOLoop.current().start()
