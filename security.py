import requests

from connexion.apps import flask_app


#
# from main import app


def verify_token(token):
    response = requests.get(
        'https://id.twitch.tv/oauth2/validate',
        headers={'Authorization': 'OAuth {}'.format(token)}
    )
    if response.status_code == requests.codes.ok:
        flask_app.logger.debug('Oauth success')

        return {'client_id': response.json, 'scope': []}
    else:
        flask_app.logger.debug('Oauth fail')

        return None
