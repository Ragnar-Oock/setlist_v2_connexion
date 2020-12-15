from models.core import Model
from pony import orm


class Song(Model):
    uuid = orm.Required(str)
