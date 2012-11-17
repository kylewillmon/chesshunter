from pyramid.view import view_config
from pyramid.httpexceptions import *
from pyramid.security import authenticated_userid
from sqlalchemy import or_

from chesshunter.models import User, DBSession, Game

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
        games = (self.session.query(Game)
                .filter(Game.state=='ongoing')
                .filter(
                    or_(User.id==Game.white_id,
                        User.id==Game.black_id))
                .all())
        return {'logged_in': True,
                'user': user,
                'games': games}
