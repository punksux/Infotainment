import json
from datetime import datetime
import re
from subprocess import Popen, PIPE
from apscheduler.scheduler import Scheduler

sched = Scheduler()
sched.start()

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
p = None
playing = False


def start_pianobar():
    global p, playing
    cmd = "pianobar"
    p = Popen(cmd, stdout=PIPE, stdin=PIPE)
    playing = True
    h = sched.add_date_job(get_pianobar_info(), datetime.now())


def get_pianobar_info():
    output = p.stdout.readline(1)
    while playing:
        if '|>  "' in output:
            print(output)
        output = p.stdin.readline(1)