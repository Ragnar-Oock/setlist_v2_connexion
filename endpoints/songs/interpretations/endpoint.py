from models import Interpretation, Song
from utils.db import format_order_by
# needed for orderby
# noinspection PyUnresolvedReferences
from pony import orm


def put(song, score):
    Interpretation(song=song, score=score)
    # return succes no content
    return '', 204


def get(song, padding, orderby, limit=50):
    interpretations = Interpretation\
        .select(lambda i: i.song == Song[song])\
        .order_by(format_order_by(orderby, 'i'))\
        .limit(limit=limit, offset=padding)
    return {'data': [i.serialize() for i in interpretations]}, 200
