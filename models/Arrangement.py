from models.core import db
from pony import orm


class Arrangement(db.Entity):
    song = orm.Set('Song')
    name = orm.Required(str, 255)
    type = orm.Required(str, 255)
    tuning = orm.Required("Tuning")
    capo = orm.Optional(int, default=0)
