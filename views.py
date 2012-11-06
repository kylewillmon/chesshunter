from pyramid.view import view_config
from pyramid.httpexceptions import *
from pyramid.security import remember, forget, authenticated_userid

from models import Game, User, DBSession
import re
from sqlalchemy import or_

import logging
logger = logging.getLogger(__name__)

class Chesshunter(object):
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.logged_in = authenticated_userid(request)

    @view_config(route_name="new_game", renderer='json',
            permission="edit", request_method="POST")
    def new_game_view(self):
        white = self.request.POST.get("white")
        black = self.request.POST.get("black")
        if not (white and
                black and
                self.session.query(User)
                    .filter(or_(User.id==white, User.id==black))
                    .count() == 2):
            raise HTTPBadRequest
        game = Game(white_id=white, black_id=black)
        self.session.add(game)
        self.session.commit()
        return game.__json__()

    @view_config(route_name="view_game", renderer='json', permission="view")
    def view_game_view(self):
        game_id = self.request.matchdict['game_id']
        game = self.session.query(Game).filter(Game.id==game_id).first()
        if not game:
            raise HTTPNotFound
        return game.__json__()

    @view_config(route_name='home', renderer='home.mak')
    def home_view(self):
        if not self.logged_in:
            url = self.request.route_url('login')
            raise HTTPFound(location=url)
        user = (self.session.query(User)
                .filter(User.id==self.logged_in).first())
        if not user:
            # Perhaps this is rude... but it only happens to deleted users
            url = self.request.route_url('logout')
            raise HTTPFound(location=url)
        all_users = self.session.query(User).all()
        return {'user': user,
                'all_users': all_users}

    @view_config(route_name='login', renderer='login.mak')
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
                    url = self.request.route_url('home')
                    raise HTTPFound(location=url, headers=headers)
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

    @view_config(route_name='register', renderer='register.mak')
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
