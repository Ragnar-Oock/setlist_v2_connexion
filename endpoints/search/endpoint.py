from pony import orm
from models import Song
from random import shuffle
from utils.db import get_random_indeces


def get(limit, padding, orderby, seed=None, search=None, lastInterpretation=None,
        interpretationNumber=None, score=None, showlights=None, vocals=None, odlc=None, arrangements=None):
    orm.set_sql_debug(True)
    search_results = orm.select(s for s in Song)

    if search:
        search_results = search_results.where(orm.raw_sql('similarity("s"."fts_col", $search) > .1'))

    if showlights:
        search_results = search_results.where(lambda s: s.showlights == showlights)

    order_by = ''
    for field in orderby:
        order_by += 's.{field},'.format(field=field)

    if seed is None:
        search_results = search_results \
            .order_by(order_by[:-1]) \
            .limit(limit=limit, offset=padding)
    else:
        indeces = get_random_indeces(orm.count(search_results), seed, limit, padding)

        # get songs based on the random indeces
        search_results = search_results \
            .where(lambda s: s.index in indeces)

        # shuffle the list
        shuffle(list(search_results))

    return {'data': [s.serialize() for s in search_results]}, 200
