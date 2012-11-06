from pyramid.config import Configurator
from pyramid.security import Allow, Authenticated, Everyone
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import models
from sqlalchemy import engine_from_config
import views
import user_views
import api_views

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
    config.add_route('new_game', '/api/new')
    config.add_route('view_game', '/api/view/{game_id}')
    config.add_route('home', '/')
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan(views)
    config.scan(user_views)
    config.scan(api_views)
    app = config.make_wsgi_app()
    return app
