import datetime
from decimal import Decimal

from models.core import db
from pony import orm


class Interpretation(db.Entity):
    song = orm.Required('Song')
    date = orm.Required(datetime.datetime, sql_default='CURRENT_TIMESTAMP')
    score = orm.Required(Decimal, precision=4, scale=2)

    def serialize(self):
        return {
            "song": self.song.id,
            "date": self.date,
            "score": self.score
        }
