import connexion
from dotenv import load_dotenv
from pony.flask import Pony

from custom_resolver.resolvers import FixedRestyResolver
from models.core import db

load_dotenv()

db.generate_mapping(create_tables=True)


app = connexion.FlaskApp(__name__, specification_dir='openapi/', debug=True)
app.add_api(
    'spec.yaml',
    resolver=FixedRestyResolver('endpoints')
)
# add pony wrapper on flask views
Pony(app.app)
app.run(port=8080, host='localhost')
