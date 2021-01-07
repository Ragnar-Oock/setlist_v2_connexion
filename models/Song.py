from models.core import db
from pony import orm


class Song(db.Entity):
    id = orm.PrimaryKey(str, 255)
    name = orm.Required(str, 255)
    artist = orm.Required(str, 255)
    album = orm.Required(str, 255)
    vocals = orm.Required(bool, default=False)

    length = orm.Optional(float, default=0)
    update_date = orm.Optional(int, default=0)
    showlights = orm.Optional(bool, default=False)
    official = orm.Optional(bool, default=False)
    custom_class = orm.Optional(str, 255, default='')
    metadata = orm.Optional(orm.Json)

    tags = orm.Set('Tag')
    arrangements = orm.Set('Arrangement')
    interpretations = orm.Set('Interpretation')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "vocals": self.vocals,
            "length": self.length,
            "official": self.official,
            "showlights": self.showlights,
            "update_date": self.update_date,
            "custom_class": self.custom_class,
        }
