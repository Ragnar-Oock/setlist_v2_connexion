from models.core import db
from pony import orm


class Arrangement(db.Entity):
    song = orm.Set('Song')
    name = orm.Required(str, 255)
    type = orm.Required(str, 255)
    tuning = orm.Required("Tuning")
    capo = orm.Optional(int, default=0)

    def serialize(self):
        return {
            "name": self.name,
            "type": self.type,
            "tuning": self.tuning.name,
            "capo": self.capo
        }
