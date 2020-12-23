from models.core import db
from pony import orm


class Tuning(db.Entity):
    arrangements = orm.Set('Arrangement')
    name = orm.Optional(str, default='Inconnu')
    string_0 = orm.Optional(int, default=0)
    string_1 = orm.Optional(int, default=0)
    string_2 = orm.Optional(int, default=0)
    string_3 = orm.Optional(int, default=0)
    string_4 = orm.Optional(int, default=0)
    string_5 = orm.Optional(int, default=0)