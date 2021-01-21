import datetime
from decimal import Decimal

from models.core import db
from pony import orm


class Interpretation(db.Entity):
    song = orm.Required('Song')
    date = orm.Required(datetime.datetime, sql_default='CURRENT_TIMESTAMP')
    score = orm.Required(Decimal, precision=4, scale=2)

    def serialize(self, show_song=False) -> dict:
        """
        serialize the current object as a dict
        :param show_song: should the parent song id be displayed
        :return: serialized Interpretation object
        """
        serialized = {
            "date": self.date,
            "score": self.score
        }
        if show_song:
            serialized["song"] = self.song.id
        return serialized
