from models import Interpretation, Song
from utils.db import format_order_by


def put(song, score):
    interpretation = Interpretation(song=song, score=score)
    # return succes no content
    return '', 204


def get(song, padding, orderby, limit=50):
    try:
        interpretations = Interpretation\
            .select(lambda i: i.song == Song[song])\
            .order_by(format_order_by(orderby, 'i'))\
            .limit(limit=limit, offset=padding)
        return {'data': [i.serialize() for i in interpretations]}, 200
    except AttributeError as e:
        return {
            'message': 'Error in orderby parameter, interpretation has no attribute \'{}\''.format(str(e).split('.')[1])
        }
