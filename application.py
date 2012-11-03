from wsgiref.simple_server import make_server

from sqlalchemy import create_engine

import models

from pyramid.config import Configurator

def main():
    engine = create_engine('sqlite:///chesshunter.db')
    models.initialize_sql(engine)
    config = Configurator()
    config.add_route('new_game', '/new')
    config.add_route('view_game', '/view/{game_id}')
    config.scan("views")
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    app = main()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
