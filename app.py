import chesshunter
import logging
import os
from wsgiref.simple_server import make_server

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('sqlalchemy').setLevel(logging.INFO)
    db = os.getenv('HEROKU_POSTGRESQL_VIOLET_URL', 'sqlite:///chesshunter.db')
    port = int(os.getenv('PORT', 8080))
    settings = {
        'auth.secret': 'chsecret',
        'sqlalchemy.url': db,
        'mako.directories': 'templates',
    }
    app = chesshunter.main({}, **settings)
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
