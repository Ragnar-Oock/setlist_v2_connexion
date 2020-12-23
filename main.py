from pony import orm
from pony.flask import Pony
from models.core import Model
from settings import db_params
import connexion
from custom_resolver.resolvers import FixedRestyResolver

app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api(
    'spec.yaml',
    resolver=FixedRestyResolver('endpoints'),

)
# add pony wrapper on flask views
Pony(app.app)
app.run(port=8080, host='localhost')

orm.set_sql_debug(True)
Model.db.bind(**db_params)
Model.db.generate_mapping(create_tables=True)
