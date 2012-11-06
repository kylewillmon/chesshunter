from pyramid.view import view_config
from pyramid.httpexceptions import *
from models import Game, User, DBSession
from sqlalchemy import or_

class api_views(object):
    def __init__(self, request):
        self.request = request
        self.session = DBSession()

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

    @view_config(route_name="view_game", renderer='json',
            permission="view")
    def view_game_view(self):
        game_id = self.request.matchdict['game_id']
        game = self.session.query(Game).filter(Game.id==game_id).first()
        if not game:
            raise HTTPNotFound
        return game.__json__()
