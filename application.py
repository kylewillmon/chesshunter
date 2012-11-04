from wsgiref.simple_server import make_server

from sqlalchemy import engine_from_config

import models

from pyramid.config import Configurator
from pyramid.security import Allow, Authenticated, Everyone
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, Authenticated, 'edit') ]

    def __init__(self, request):
        pass

def main(global_config, **settings):
    engine = engine_from_config(settings)
    models.initialize_sql(engine)

    authn_policy = AuthTktAuthenticationPolicy(
            settings['auth.secret'])
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
            authentication_policy=authn_policy,
            authorization_policy=authz_policy,
            root_factory=RootFactory)
    config.add_route('new_game', '/new')
    config.add_route('view_game', '/view/{game_id}')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan("views")
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    settings = {
        'auth.secret': 'chsecret',
        'sqlalchemy.url': 'sqlite:///chesshunter.db',
        'sqlalchemy.echo': True,
    }
    app = main({}, **settings)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
