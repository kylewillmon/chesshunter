from pyramid.view import view_config
from pyramid.httpexceptions import *
from pyramid.security import remember, forget, authenticated_userid
from chesshunter.models import User, DBSession
import re

@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    url = request.route_url('home')
    raise HTTPFound(location=url, headers=headers)

class user_views(object):
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.logged_in = authenticated_userid(request)

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
