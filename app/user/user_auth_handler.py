#! -*- coding:utf8 -*-

import tornado.web
#from user.models.user import UserDAO
import tornado.ioloop
import simplejson
import sys
sys.path.append("..")
from utils.db_helper import DB42
from models.user_passport import PassportDAO
from models.user import UserDAO
from views.user_view import UserView

class AuthHandler(tornado.web.RequestHandler):
    '''
    # 登陆验证的handler
    # 验证成功     : 返回票和用户信息
    # 验证失败     : 返回 401 error_code
    # Router      : r"/user/auth" POST
    # ParamField  : account, password
    '''
    # def post(self):
    def get(self):
        account = self.get_query_argument("account")
        password = self.get_query_argument("password")
        # t = authenticate(account, password)
        user_passport = PassportDAO().GetByAccountPassword(account, password)
        if user_passport:
            ids=[]
            ids.append(user_passport._id)
            users = UserDAO().GetByIds(ids)
            if users and len(users) > 0:
                self.write(map(lambda x : UserView(x).to_json(),users)[0])
        else:
            self.write("401, authentication failure!")



application = tornado.web.Application([
	(r"/user/auth", AuthHandler),
])

if __name__ == "__main__":
	application.listen(8081)
	tornado.ioloop.IOLoop.current().start()
