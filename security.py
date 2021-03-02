import requests
import logging
import os

logger = logging.getLogger(__name__)


def verify_token(token):
    # validate the token with the Twitch API
    response = requests.get(
        'https://id.twitch.tv/oauth2/validate',
        headers={'Authorization': 'OAuth {}'.format(token)}
    )

    # the token is a valide token
    if response.status_code == requests.codes.ok:
        body = response.json()

        # the token belong to this application
        if body['client_id'] == os.environ['CLIENT_ID']:

            # if the token is not a implicit code flow token (there's no user info in the response)
            if body.get('user_id') is None and body.get('login') is None:
                logger.info('Oauth success')

                return {'client_id': response.json, 'scope': []}
            # there's user info in the response, not a client credential flow token, reject the request
            else:
                return None

        # the token doesn't belong to this application, reject the request
        else:
            logger.info('Oauth fail, token has been generated with an unknown client id : {}'.format(body['client_id']))
            return None

    # the validation request failed
    else:
        logger.info('Oauth fail, token is invalid')
        return None
