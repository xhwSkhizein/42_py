#! -*- coding:utf8 -*-

import MySQLdb
import threading
import Queue
import tornado.ioloop
from tornado import gen
from tornado.log import gen_log
from functools import partial

class DB42(object):
    def __init__(self, host='127.0.0.1', port='3306', #
                    user=None, passwd=None, dbname=None, #
                    pool_size=8, ioloop=None):
        self._threads = [] # 线程池
        self._working = True
        self._tasks = Queue.Queue() # 正在执行的任务队列
        self.ioloop = ioloop
        # 数据库连接配置
        self._config = cn = {}
        cn['host'] = host
        cn['port'] = port
        if user: cn['user'] = user
        if passwd: cn['passwd'] = passwd
        if dbname: cn['db'] = dbname
        # create threads
        for i in xrange(pool_size):
            t = Worker(self)
            t.start()
            self._threads.append(t)
    def do_inner_update(self, sql, argvs=None, callback=None):
        assert callback
        # 标准task是一个list，第一项是执行的任务类型，
        # 第二项是执行的sql语句，点三项是sql语句参数，第四项是执行后的回调方法
        self._tasks.put(['query', sql, argvs, callback])
    def do_inner_query(self, sql, argvs=None, callback=None):
        assert callback
        gen_log.info("存入tasks，command={0},sql={1}, argvs={2}",['query', sql, argvs])
        self._tasks.put(['query', sql, argvs, callback])
    # 创建update
    def update(self, sql, argvs=None):
        return gen.Task(self.do_inner_update, sql, argvs)
    # 创建query
    def query(self, sql, argvs=None):
        return gen.Task(self.do_inner_query, sql, argvs)
    # 将结果返回
    def send_result(self, task, result, error):
        callback = partial(task[3], (result, error))
        ioloop = self.ioloop or tornado.ioloop.IOLoop.instance()
        ioloop.add_callback(callback)
    def stop(self):
        self._working = False
        self._tasks.put(['stop'])
        map(lambda t: t.join(), self._threads)



class Worker(threading.Thread):
    def __init__(self, ctx):
        self._conn = None
        self._ctx = ctx
        super(Worker, self).__init__()
    def get_cursor(self):
        # FIXME 判断连接时间是否需要重新连接,不需要的话直接返回
        if self._conn and self._conn.open:
            self._conn.close()
        self._conn = MySQLdb.connect(
                    use_unicode=True, charset='utf8', **self._ctx._config)
        self._conn.autocommit(True)
        return self._conn.cursor()
    def close_conn(self):
        if self._conn:
            self._conn.close()
            self._conn = None
    def run(self):
        ctx = self._ctx
        while ctx._working:
            result = None
            error = None
            cursor = None
            try:
                task = ctx._tasks.get(True) # 如果取不到就阻塞 FIXME 可以适当扩容
                command_type = task[0]
                gen_log.info("command={0}",[command_type])
                if command_type == 'stop':
                    # 没有任务返回
                    break
                sql = task[1]
                argvs = task[2] or []
                cursor = self.get_cursor()
                if command_type == 'query':
                    cursor.execute(sql, argvs)
                    result = cursor.fetchall()
                else:
                    cursor.execute(sql, argvs)
            except Exception as e:
                error = e
            finally:
                if cursor: cursor.close()
            gen_log.info("执行完毕，返回，command={0},sql={1}, argvs={2}",[command_type, sql, argvs])
            ctx.send_result(task, result, error)
        gen_log.info("准备关闭所有持有的连接...")
        print "准备关闭所有持有的连接..."
        # 关闭时关闭持有的连接
        self.close_conn()


if '__main__' == __name__:
    pass
