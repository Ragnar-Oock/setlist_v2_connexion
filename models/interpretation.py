import datetime
from decimal import Decimal

from models.core import db
from pony import orm


class Interpretation(db.Entity):
    song = orm.Required('Song')
    date = orm.Optional(datetime.datetime, default=datetime.datetime.now())
    score = orm.Required(Decimal, precision=4, scale=2)
