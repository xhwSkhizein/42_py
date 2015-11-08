import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")
	def post(self):
		self.write("post hello, world...")

class AuthHandler(tornado.web.RequestHandler):
	def get(self):
		print(dir(self))
		print(type(self))
		print("name: " + self.get_argument("name"));
		print("passwd: " + self.get_argument("passwd"));
		self.write("lalal");


application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/auth", AuthHandler),
])

if __name__ == "__main__":
	application.listen(8081)
	tornado.ioloop.IOLoop.current().start()
