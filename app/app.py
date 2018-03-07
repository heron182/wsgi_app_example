import logging
from cgi import escape, parse_qs
from wsgiref.simple_server import make_server

logging.basicConfig(level=logging.INFO)

PORT = 8080
HOST = 'localhost'


class App(object):
    def __init__(self, router):
        self.router = router

    def __call__(self, environ, start_response):
        for path, callable in self.router.routes:
            if path == environ['PATH_INFO']:
                start_response('200 OK',
                               [('Content-Type', 'text/html; charset=utf-8')])
                return callable(environ, start_response)
        start_response('404 NOT FOUND',
                       [('Content-Type', 'text/html; charset=utf-8')])
        return ['Página não encontrada'.encode('utf-8')]


class Route(object):
    def __init__(self, path, callable):
        self.path, self.callable = path, callable


class Router(object):
    def __init__(self):
        self.routes = []

    def attach_route(self, path, callable):
        self.routes.append((path, callable))


def index(environ, start_response):
    return ['<h1> Index Page </h1>'.encode('utf-8')]


def products(environ, start_response):
    return ['<h1> Products page </h1>'.encode('utf-8')]


if __name__ == '__main__':
    index = Route('/', index)
    products = Route('/products', products)
    router = Router()
    router.attach_route(index.path, index.callable)
    router.attach_route(products.path, products.callable)
    app = App(router)
    logging.info(f'Serving App on http://{HOST}:{PORT}')
    srv = make_server(HOST, PORT, app)
    srv.serve_forever()
