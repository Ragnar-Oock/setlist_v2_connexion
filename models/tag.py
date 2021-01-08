from models.core import db
from pony import orm


class Tag(db.Entity):
    song = orm.Set('Song')
    name = orm.Required(str, 255, unique=True)
    color = orm.Required(str, 6)

    @staticmethod
    def add_entry(name, color):
        existing_tag = Tag.select(
            lambda t:
            t.name == name
        ).limit(1)

        if existing_tag:
            return existing_tag[0]
        else:
            tag = Tag(name=name, color=color)
            # save tag to the DB and return
            db.flush()
            return tag
