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

    # --- arrangement specific fields ---
    # does the song have certain arrangements
    if arrangements:
        search_results = search_results.where(lambda s: orm.JOIN(arrangements[0] in s.arrangements.type))

    # --- interpretation specific fields ---
    # how many times does the song was played
    if interpretationNumber != [0, 100]:
        lower_bound = min(interpretationNumber[0], interpretationNumber[1])
        upper_bound = max(interpretationNumber[0], interpretationNumber[1])
        print(lower_bound, ' - ', upper_bound)
        search_results = search_results.where(
            lambda s:
                lower_bound <= orm.count(s.interpretations)
                and (orm.count(s.interpretations) <= upper_bound or upper_bound >= 100)
        )

    # apply order by, limit and padding
    search_results = search_results \
        .order_by(format_order_by(orderby)) \
        .limit(limit=limit, offset=padding)

    return {'data': [s.serialize() for s in search_results]}, 200
