from pony import orm
from models import Song
from utils.db import format_order_by
from datetime import timedelta, datetime
from decimal import Decimal


def get(search, lastInterpretation=None,
        interpretationNumber=None, score=None, showlights=None, vocals=None, odlc=None, arrangements=None):
    orm.set_sql_debug(True)

    # song search
    # region
    # fuzzy search
    song_results = orm.select(s for s in Song).where(orm.raw_sql('similarity("s"."fts_col", $search) > .1'))

    # does the song has showlights
    if showlights:
        song_results = song_results.where(lambda s: s.showlights == showlights)

    # does the song display lyrics
    if vocals:
        song_results = song_results.where(lambda s: s.vocals == vocals)

    # is the song a odlc or a cdlc
    if odlc is not None:
        song_results = song_results.where(lambda s: s.official == odlc)

    # --- arrangement specific fields ---
    # does the song have certain arrangements
    if arrangements:
        filter_function = ''
        for i in range(0, len(arrangements)):
            filter_function += 'or arrangements[{}] in s.arrangements.type '.format(i)
        filter_function = filter_function.split('or ', 1)[1]

        song_results = song_results.where(filter_function)

    # --- interpretation specific fields ---
    # how many times does the song was played
    if interpretationNumber != [0, 100]:
        lower_bound = min(interpretationNumber[0], interpretationNumber[1])
        upper_bound = max(interpretationNumber[0], interpretationNumber[1])
        song_results = song_results.where(
            lambda s:
            lower_bound <= orm.count(s.interpretations)
            and (orm.count(s.interpretations) <= upper_bound or upper_bound >= 100)
        )

    if lastInterpretation != [0, 100]:
        # higher bound in days to allow no maximum calculation when >=100
        upper_bound = max(lastInterpretation[0], lastInterpretation[1])
        # datetime bounds to be used in where clause
        older_bound = datetime.now() - timedelta(days=max(lastInterpretation[0], lastInterpretation[1]))
        youger_bound = datetime.now() - timedelta(days=min(lastInterpretation[0], lastInterpretation[1]))

        song_results = song_results.where(
            lambda s:
            youger_bound > orm.max(s.interpretations.date)
            and (orm.max(s.interpretations.date) <= older_bound or upper_bound >= 100)
        )

    if score != [0, 100]:
        lower_bound = Decimal(min(score[0], score[1]))
        upper_bound = Decimal(max(score[0], score[1]))
        song_results = song_results.where(
            lambda s:
            lower_bound <= orm.max(s.interpretations.score) and orm.max(s.interpretations.score) <= upper_bound
        )

    # apply order by, limit and padding
    song_results = song_results \
        .order_by(format_order_by(['-similarity', 'name', 'album', 'artist'])) \
        .limit(limit=5)
    # endregion

    # artists search
    artist_results = orm.select((s.artist, orm.raw_sql('similarity("s"."artist", $search)')) for s in Song) \
        .distinct() \
        .where(orm.raw_sql('similarity("s"."artist", $search) > .1')) \
        .order_by(format_order_by(['-similarity', 'artist'], similarity_col='artist')) \
        .limit(limit=5)

    return {'data': {
        'song': [s.make_song_suggestion() for s in song_results],
        'artist': [{'name': a[0]} for a in artist_results]
    }}, 200
