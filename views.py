from pyramid.view import view_config
from pyramid.httpexceptions import *

from models import Game, User, DBSession

@view_config(route_name="new_game", renderer='json', permission="edit")
def new_game(request):
    session = DBSession()
    game = Game(white="kylewillmon", black="sheerluck")
    session.add(game)
    session.commit()
    return {'status': 'success',
            'game': game.__json__()}

@view_config(route_name="view_game", renderer='json', permission="view")
def view_game(request):
    session = DBSession()
    game_id = request.matchdict['game_id']
    game = session.query(Game).filter(Game.id==game_id).first()
    if not game:
        raise HTTPNotFound
    return {'status': 'success',
            'game': game.__json__()}

@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
    session = DBSession()
    message = 'Please log in'
    if 'submit' in request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = session.query(User).filter(User.username==username).first()
        if user:
            if user.check_password(password):
                message = "Success"
            else:
                message = 'Fail'
        else:
            message = 'Invalid user'
    return {'message': message}
