from models.core import db
from pony import orm


class Tuning(db.Entity):
    arrangements = orm.Set('Arrangement')
    name = orm.Optional(str, default='Inconnu')
    string_0 = orm.Required(int, default=0)
    string_1 = orm.Required(int, default=0)
    string_2 = orm.Required(int, default=0)
    string_3 = orm.Required(int, default=0)
    string_4 = orm.Required(int, default=0)
    string_5 = orm.Required(int, default=0)

    @staticmethod
    def add_entry(strings):
        existingTuning = Tuning.select(
            lambda t:
            t.string_0 == strings[0]
            and t.string_1 == strings[1]
            and t.string_2 == strings[2]
            and t.string_3 == strings[3]
            and t.string_4 == strings[4]
            and t.string_5 == strings[5]
        ).limit(1)

        if existingTuning:
            return existingTuning[0]
        else:
            tuning = Tuning(
                string_0=strings[0],
                string_1=strings[1],
                string_2=strings[2],
                string_3=strings[3],
                string_4=strings[4],
                string_5=strings[5],
            )
            # save tuning to the db and return
            db.flush()
            return tuning
