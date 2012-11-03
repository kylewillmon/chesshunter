from pyramid.view import view_config
from pyramid.httpexceptions import *

from models import Game, DBSession

@view_config(route_name="new_game", renderer='json')
def new_game(request):
    session = DBSession()
    game = Game(white="kylewillmon", black="sheerluck")
    session.add(game)
    session.commit()
    return {'status': 'success',
            'game': game.__json__()}

@view_config(route_name="view_game", renderer='json')
def view_game(request):
    session = DBSession()
    game_id = request.matchdict['game_id']
    game = session.query(Game).filter(Game.id==game_id).first()
    if not game:
        raise HTTPNotFound
    return {'status': 'success',
            'game': game.__json__()}
