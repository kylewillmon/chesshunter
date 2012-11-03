from pyramid.view import view_config
from pyramid.httpexceptions import *

from models import Game

@view_config(name="new", renderer='json')
def new_game(request):
    return {'response': 'Hello, World!'}
