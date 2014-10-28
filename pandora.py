import json
from datetime import datetime
import re

artist = ''
album = ''

last_fm_api = '7e0ead667c3b37eb1ed9f3d16778fe38'
last_fm_website = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=7e0ead667c3b37eb1ed9f3d16778fe38&' \
                  'artist=%s&album=%s&format=json' % (artist, album)


def get_album(artist2, album2):
    global artist, album
    artist = artist2
    album = album2
    f = open('album_info.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    album_art = parsed_json['album']['image'][3]['#text']
    album_sum = re.sub('<[^<]+?>', '', parsed_json['album']['wiki']['summary'])
    album_release = datetime.strptime(parsed_json['album']['releasedate'], '    %d %b %Y, %H:%M')
    return [album_art, album_release.strftime('%B %d, %Y'), album_sum]

#print(get_album('1', '1'))