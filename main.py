import connexion
from dotenv import load_dotenv
from flask_cors import CORS
from pony.flask import Pony

from custom_resolver.resolvers import FixedRestyResolver
from models.core import db

os.chdir(os.path.dirname(os.path.realpath(__file__)))
load_dotenv(".env.local")
load_dotenv(".env")

db.generate_mapping(create_tables=True)


app = connexion.FlaskApp(__name__, specification_dir='openapi/', debug=True)
app.add_api(
    'spec.yaml',
    resolver=FixedRestyResolver('endpoints')
)
# add pony wrapper on flask views
CORS(app.app)
Pony(app.app)

if __name__ == "__main__":
    app.run(port=8080, host='localhost')
