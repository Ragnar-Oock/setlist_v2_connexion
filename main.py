from pony import orm
from pony.flask import Pony
from models.core import Model
from settings import db_params
import connexion
from connexion.resolver import RestyResolver

app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api(
    'spec.yaml',
    resolver=RestyResolver('endpoints'),

)
app.run(port=8080)
# add pony wrapper on flask views
Pony(app)

orm.set_sql_debug(True)
Model.db.bind(**db_params)
Model.db.generate_mapping(create_tables=True)
