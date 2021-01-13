from pony import orm
from models import Song
from random import shuffle
from utils.db import get_random_indeces


def get(limit, padding, orderby, seed=None):
    order_by = ''
    for field in orderby:
        order_by += 's.{field},'.format(field=field)

    if seed is None:
        song_list = orm\
            .select(s for s in Song)\
            .order_by(order_by[:-1])\
            .limit(limit=limit, offset=padding)
        indeces = []
    else:
        indeces = get_random_indeces(orm.count(s for s in Song), seed, limit, padding)

        # get songs based on the random indeces
        song_list = orm\
            .select(s for s in Song)\
            .where(lambda s: s.index in indeces)

        # shuffle the list
        shuffle(list(song_list))

    return {'data': [s.serialize() for s in song_list]}, 200


def put(body):
    for song in body:
        print(song)
        try:
            Song.add_entry(song)
        except Exception:
            orm.rollback()
            return {"message": "failed to insert the song of id {}".format(song.get('id'))}, 400

    return {"message": "Sucssfully inserted {} songs".format(len(body))}, 200


def delete(ids):
    try:
        for song_id in ids:
            Song[song_id].delete()
        # return 204 sucess no content response
        return '', 204
    # prevent error if a record to be deleted is missing
    except orm.core.ObjectNotFound:
        return '', 204
