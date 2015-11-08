#! -*- coding:utf8 -*-
# 用户验证
#

import tornado.web
import tornado.ioloop
import simplejson
import sys
sys.path.append("..")
from base.db_helper import DB42
from models.user_passport import PassportDAO
from models.user import UserDAO
from models.ticket import TicketService
from views.user_view import UserView
from base.response import ResponseWrapper

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
        user_passport = PassportDAO().GetByAccountPassword(account, password)
        if user_passport:
            ids=[]
            ids.append(user_passport._id)
            users = UserDAO().GetByIds(ids)
            if users and len(users) > 0:
                userview = map(lambda x : UserView(x).to_json(),users)[0]
                response = ResponseWrapper().add("user", userview)
                ticket = TicketService.get_ticket(user_passport._id)
                print ticket
                if ticket:
                    response.add("t", ticket)
                # TODO 添加currenUser到header
                self.write(response.to_json())
        else:
            response = ResponseWrapper("authentication failure!", 401)
            self.write(response.to_json())



application = tornado.web.Application([
	(r"/user/auth", AuthHandler),
])

if __name__ == "__main__":
	application.listen(8081)
	tornado.ioloop.IOLoop.current().start()
