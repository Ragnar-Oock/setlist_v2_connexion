from pony import orm
from models import Song
from utils.db import format_order_by


def get(limit, padding, orderby: list, search=None, lastInterpretation=None,
        interpretationNumber=None, score=None, showlights=None, vocals=None, odlc=None, arrangements=None):
    orm.set_sql_debug(True)
    search_results = orm.select(s for s in Song)

    # fuzzy search
    if search:
        search_results = search_results.where(orm.raw_sql('similarity("s"."fts_col", $search) > .1'))
        # add similarity to the order by array
        orderby.insert(0, '-similarity')

    # does the song has showlights
    if showlights:
        search_results = search_results.where(lambda s: s.showlights == showlights)

    # does the song display lyrics
    if vocals:
        search_results = search_results.where(lambda s: s.vocals == vocals)

    # is the song a odlc or a cdlc
    if odlc is not None:
        search_results = search_results.where(lambda s: s.official == odlc)

        # get songs based on the random indeces
        search_results = search_results \
            .where(lambda s: s.index in indeces)

    # apply order by, limit and padding
    search_results = search_results \
        .order_by(format_order_by(orderby)) \
        .limit(limit=limit, offset=padding)

    return {'data': [s.serialize() for s in search_results]}, 200
