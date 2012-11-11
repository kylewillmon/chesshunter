from pyramid.config import Configurator
from pyramid.security import Allow, Authenticated, Everyone
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import models
from sqlalchemy import engine_from_config
import views

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
    config.add_route('games', '/api/games')
    config.add_route('view_game', '/api/games/{game_id}')
    config.add_route('make_move', '/api/games/{game_id}/move')
    config.add_route('resign', '/api/games/{game_id}/resign')
    config.add_route('offer_draw', '/api/games/{game_id}/offerdraw')
    config.add_route('accept_draw', '/api/games/{game_id}/acceptdraw')
    config.add_route('users', '/api/users')
    config.add_route('view_user', '/api/users/{user_id}')
    config.add_route('home', '/')
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan(views)
    app = config.make_wsgi_app()
    return app
