from models import Interpretation, Song


def put(song, score):
    interpretation = Interpretation(song=song, score=score)
    # return succes no content
    return '', 204


def get(song):
    interpretations = Interpretation.select(lambda i: i.song == Song[song])
    return {'data': [i.serialize() for i in interpretations]}, 200
