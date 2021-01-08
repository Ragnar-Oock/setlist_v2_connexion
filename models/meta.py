from models.core import db
from pony import orm


class Meta(db.Entity):
    song = orm.Required('Song')
    key = orm.Required(str, 255)
    value = orm.Required(str, 255)
