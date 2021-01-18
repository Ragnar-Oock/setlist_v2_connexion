from models import Interpretation


def put(song, score):
    interpretation = Interpretation(song=song, score=score)
    return 'put interpretation'


def get():
    return 'get interpretation'
