from pony import orm
from models import Song
from flask import jsonify
from models.core import db


def get(limit, padding, orderby, seed):
    song_list = Song.select()
    q = {'data': [s.serialize() for s in song_list]}
    return jsonify(q)


def put(body):
    for song in body:
        try:
            Song.add_entry(song)
            db.flush()
        except Exception:
            return ['prout'], 400

    return 'im a put'


def delete(ids):
    try:
        for song_id in ids:
            Song[song_id].delete()
        # return 204 sucess no content response
        return '', 204
    # prevent error if a record to be deleted is missing
    except orm.core.ObjectNotFound:
        return '', 204
