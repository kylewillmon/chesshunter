from pyramid.view import view_config
from pyramid.httpexceptions import *
from pyramid.security import authenticated_userid

from chesshunter.models import User, DBSession

from user import *
from api import *

class main_views(object):
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.logged_in = authenticated_userid(request)

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
