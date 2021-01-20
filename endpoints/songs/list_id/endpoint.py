from models.core import db


def get():
    # select all song ids from the database
    id_list = db.select('select id from song')
    return {'data': id_list}, 200
