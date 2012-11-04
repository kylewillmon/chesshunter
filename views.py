from pyramid.view import view_config
from pyramid.httpexceptions import *
from pyramid.security import remember, forget, authenticated_userid

from models import Game, User, DBSession
import re

import logging
logger = logging.getLogger(__name__)

class Chesshunter(object):
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.logged_in = authenticated_userid(request)

    @view_config(route_name="new_game", renderer='json', permission="edit")
    def new_game_view(self):
        game = Game(white="kylewillmon", black="sheerluck")
        self.session.add(game)
        self.session.commit()
        return {'status': 'success',
                'game': game.__json__()}

    @view_config(route_name="view_game", renderer='json', permission="view")
    def view_game_view(self):
        game_id = self.request.matchdict['game_id']
        game = self.session.query(Game).filter(Game.id==game_id).first()
        if not game:
            raise HTTPNotFound
        return {'status': 'success',
                'game': game.__json__()}

    @view_config(route_name='home', renderer='templates/home.pt')
    def home_view(self):
        return {}

    @view_config(route_name='login', renderer='templates/login.pt')
    def login_view(self):
        message = 'Please log in'
        if self.logged_in:
            url = self.request.route_url('home')
            raise HTTPFound(location=url)
        if 'submit' in self.request.POST:
            username = self.request.POST.get('username', '')
            password = self.request.POST.get('password', '')
            user = (self.session.query(User)
                    .filter(User.username==username).first())
            if user:
                if user.check_password(password):
                    headers = remember(self.request, user.id)
                    raise HTTPFound(location='/', headers=headers)
                else:
                    message = 'Invalid password'
            else:
                message = 'Invalid user'
        return {'message': message}

    @view_config(route_name='logout')
    def logout_view(self):
        headers = forget(self.request)
        url = self.request.route_url('home')
        raise HTTPFound(location=url, headers=headers)

    @view_config(route_name='register', renderer='templates/register.pt')
    def register_view(self):
        error = None
        message = None
        if 'submit' in self.request.POST:
            username = self.request.POST.get('username')
            password = self.request.POST.get('password')
            if not username or not re.match('^\w+$', username):
                error = 'Invalid username'
            else:
                user = (self.session.query(User)
                        .filter(User.username==username).first())
                if user:
                    error = 'Username in use'
                else:
                    user = User(username, password)
                    self.session.add(user)
                    self.session.commit()
                    message = 'User "%s" successfully created' % username
        return {'error': error,
                'message': message}
