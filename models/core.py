from pony import orm
from settings import db_params

db = orm.Database(**db_params)
