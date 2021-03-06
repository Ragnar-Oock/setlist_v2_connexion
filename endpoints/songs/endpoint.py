from pony import orm
from pony.orm import IntegrityError

from models import Song
from random import shuffle, seed as set_seed
from utils.db import format_order_by
from pony.orm.core import TransactionIntegrityError

import time
import logging

logger = logging.getLogger(__name__)


def get(limit, padding, orderby, seed=None):
    if seed is None:
        song_list = orm \
            .select(s for s in Song) \
            .order_by(format_order_by(orderby)) \
            .limit(limit=limit, offset=padding)
    else:
        # shuffle all results
        id_list = list(orm.select(s.id for s in Song))
        set_seed(a=seed, version=2)
        shuffle(id_list)
        song_list = orm.select(s for s in Song).where(lambda s: s.id in id_list[padding:padding + limit])

    return {'data': [s.serialize() for s in song_list]}, 200


def put(body):
    for song in body:
        try:
            Song.add_entry(song)
        except IntegrityError:
            orm.rollback()
            return {"message": "song of id {} already exists, aborting insert".format(song.get('id'))}, 400
        except TransactionIntegrityError:
            orm.rollback()
            return {"message": "song of id {} already exists, aborting insert".format(song.get('id'))}, 400
        except Exception as e:
            orm.rollback()
            logger.error(e)
            return {
                       "message": "failed to insert the song of id {}, unknown error, check log for more info."
                                  " TIMESTAMP {}".format(song.get('id'), time.asctime())
                   }, 400

    return {"message": "Successfully inserted {} songs".format(len(body))}, 200


def delete(ids):
    try:
        for song_id in ids:
            Song[song_id].delete()
        # return 204 sucess no content response
        return '', 204
    # prevent error if a record to be deleted is missing
    except orm.core.ObjectNotFound:
        return '', 204
