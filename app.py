from tornado.web import Application as BaseApplication
from tornado.log import gen_log

#
class Application(BaseApplication):
    def __init__(self, handlers=None, default_host='', transforms=None, **settings):
        super(Application, self).__init__(
            handlers=handlers, default_host=default_host,
            transforms=transforms, **settings)
            gen_log.info('Application start config: settings={0}, handlers={1}, default_host={2}'.format(settings, handlers, default_host));
