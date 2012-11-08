from pyramid.view import view_config
from pyramid.httpexceptions import *
from chesshunter.models import Game, Move, User, DBSession
from sqlalchemy import or_
import chess

class api_views(object):
    def __init__(self, request):
        self.request = request
        self.session = DBSession()

    @view_config(route_name="games", renderer='json',
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
        game = Game(board=chess.Game().fen(),
                white_id=white, black_id=black)
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

    @view_config(route_name="make_move", renderer='json',
            permission="edit", request_method="POST")
    def make_move_view(self):
        src = self.request.POST.get("src")
        dst = self.request.POST.get("dst")
        game_id = self.request.matchdict['game_id']
        game = self.session.query(Game).filter(Game.id==game_id).first()
        if not game:
            raise HTTPNotFound
        g = chess.Game(fen=game.board)
        try:
            move = chess.BasicMove(src, dst)
            g.validate_move(move)
        except:
            raise HTTPBadRequest
        move_num = g.fullmove + (1 if g.active == 'b' else 0)
        game.moves.append(Move(
            move_num=move_num,
            game_id=game_id,
            src=src,
            dst=dst))
        game.board = g.move(move).fen()
        self.session.commit()
        return game.__json__()
