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

@view_config(route_name='register', renderer='register.mak',
        request_method="GET")
def register_get_view(self):
    return dict(error="", message="")

class user_views(object):
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.logged_in = authenticated_userid(request)

    @view_config(route_name='login', renderer='login.mak',
            request_method="GET")
    def login_get_view(self):
        if self.logged_in:
            url = self.request.route_url('home')
            raise HTTPFound(location=url)
        return {'logged_in': False, 'message': ''}

    @view_config(route_name='login', renderer='login.mak',
            request_method="POST")
    def login_post_view(self):
        message = ''
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
        return {'logged_in': False, 'message': message}

    @view_config(route_name='register', renderer='register.mak',
            request_method="POST")
    def register_post_vies(self):
        error, message = "", ""
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
                user = User.new(username, password)
                self.session.add(user)
                self.session.commit()
                message = 'User "%s" successfully created' % username
        return  dict(error=error,message=message)
