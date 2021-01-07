from models import Song, Arrangement
from flask import jsonify
import json


def get(limit, padding, orderby, seed):
    song_list = Song.select()
    q = {'data': [s.to_dict() for s in song_list]}
    return jsonify(q)
    # return 'prout'


def put(body):
    print(body)
    songs = json.load(body)
    new_songs = []
    try:
        for song in songs:
            new_song = Song(
                id=song['id'],
                name=song['name'],
                artist=song['artist'],
                album=song['album'],
                vocals=song['vocals']
            )
            if song['length']:
                new_song.length = song['length']
            if song['update_date']:
                new_song.update_date = song['update_date']
            if song['showlights']:
                new_song.showlights = song['showlights']
            if song['official']:
                new_song.official = song['official']
            if song['custom_class']:
                new_song.custom_class = song['custom_class']
            if song['arrangements']:
                arrangement_list = []
                for arrangement in song['arrangements']:
                    new_arrangement = Arrangement(
                        song=new_song,
                        name=arrangement['name'],
                        type=arrangement['type'],
                        tuning=arrangement['tuning']
                    )
                    if arrangement['capo']:
                        new_arrangement.capo = arrangement['capo']
                    arrangement_list.append(new_arrangement)
                new_song.arrangements = arrangement_list
            if song['tags']:
                pass
                # TODO: implement get or create tag
                # tag_list = []
                # for tag in song['tag']:
                #     new_tag = Tag

    except Exception as e:
        print(e)
    return 'im a put'


def delete(ids):
    try:
        for song_id in ids:
            Song[song_id].delete()
        # return 204 sucess no content response
        return '', 204
    # prevent error if a record to be deleted is missing
    except orm.core.ObjectNotFound:
        return '', 204
