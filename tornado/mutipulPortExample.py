#coding: utf8
# fact.py
import tornado.ioloop
import tornado.web


"""
下面我们编写一个正常的web服务器，它将提供阶乘服务。也就是帮我们计算n!的值。
服务器会提供阶乘的缓存，已经计算过的就存起来，下次就不用重新计算了。
使用Python的好处就是，我们不用当心阶乘的计算结果会溢出，Python的整数可以无限大。
本示例摘自掘金，采用单实例多端口服务器并发
"""


class FactorialService(object):  # 定义一个阶乘服务对象

    def __init__(self):
        self.cache = {}   # 用字典记录已经计算过的阶乘

    def calc(self, n):
        if n in self.cache:  # 如果有直接返回
            return self.cache[n]
        s = 1
        for i in range(1, n):
            s *= i
        self.cache[n] = s  # 缓存起来
        return s


class FactorialHandler(tornado.web.RequestHandler):

    service = FactorialService()  # new出阶乘服务对象

    def get(self):
        n = int(self.get_argument("n"))  # 获取url的参数值
        self.write(str(self.service.calc(n)))  # 使用阶乘服务


def make_app():
    return tornado.web.Application([
        (r"/fact", FactorialHandler),  # 注册路由
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(10000)
    app.listen(10001)
    app.listen(10002)
    tornado.ioloop.IOLoop.current().start()

