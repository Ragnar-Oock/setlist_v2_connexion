from models.core import db
from pony import orm


class Tag(db.Entity):
    song = orm.Set('Song')
    name = orm.Required(str, 255)
    color = orm.Required(str, 6)
