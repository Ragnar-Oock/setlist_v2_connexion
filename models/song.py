from .core import db
from pony import orm
from .tuning import Tuning
from .tag import Tag
from .arrangement import Arrangement


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
    metadata = orm.Optional(orm.Json, default={})

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
            "metadata": self.metadata,

            "tags": [t.to_dict() for t in self.tags],
            "arrangements": [a.serialize() for a in self.arrangements]
        }

    @staticmethod
    def add_entry(entry):
        # create the song object
        new_song = Song(
            id=entry.get('id'),
            name=entry.get('name'),
            artist=entry.get('artist'),
            album=entry.get('album'),
            vocals=entry.get('vocals'),
            metadata=entry.get('metadata')
        )

        # handle arrangements
        if entry.get('arrangements'):
            arrangement_list = []
            # create all arrangements
            for arrangement in entry['arrangements']:
                new_arrangement = Arrangement(
                    song=new_song,
                    name=arrangement['name'],
                    type=arrangement['type'],
                    tuning=Tuning.add_entry(arrangement['tuning'])
                )
                if arrangement['capo']:
                    new_arrangement.capo = arrangement['capo']
                arrangement_list.append(new_arrangement)
            # add all arrangements to the song
            new_song.arrangements = arrangement_list

        # handle tags
        if entry.get('tags'):
            tag_list = []
            # get or create all tags
            for tag in entry['tags']:
                tag_list = Tag.add_entry(tag.get('name'), tag.get('color'))
            # add all tags to the song
            new_song.tags = tag_list
