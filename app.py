import chesshunter
import logging
from wsgiref.simple_server import make_server

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('sqlalchemy').setLevel(logging.INFO)
    settings = {
        'auth.secret': 'chsecret',
        'sqlalchemy.url': 'sqlite:///chesshunter.db',
        'mako.directories': 'templates',
    }
    app = chesshunter.main({}, **settings)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
