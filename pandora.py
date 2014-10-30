import json
from datetime import datetime
import re
from subprocess import Popen, PIPE
from apscheduler.scheduler import Scheduler
from info import get_album_info

on_pi = False

if on_pi:
    import pexpect

sched = Scheduler()
sched.start()

artist = ''
album = ''
song = ''
information = []
info_old = []

last_fm_api = '7e0ead667c3b37eb1ed9f3d16778fe38'
last_fm_website = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=7e0ead667c3b37eb1ed9f3d16778fe38&' \
                  'artist=%s&album=%s&format=json' % (artist, album)


def get_album(song2, artist2, album2):
    f = open('album_info.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    album_art = parsed_json['album']['image'][3]['#text']
    album_sum = re.sub('<[^<]+?>', '', parsed_json['album']['wiki']['summary'])
    get_album_info(song2, artist2, album2, album_art, album_sum)

#print(get_album('1', '1'))
p = None
h = None
playing = False
pianobar = None


def start_pianobar():
    global pianobar
    pianobar = pexpect.spawn('sudo -u pi pianobar')
    h = sched.add_interval_job(get_pianobar_info, 120)


def get_pianobar_info():
    sched.unschedule_job(h)
    global artist, album, song, information, info_old
    pattern_list = pianobar.compile_pattern_list(['SONG: ', 'STATION: ', 'TIME: '])

    while pianobar.isalive():
        # Process all pending pianobar output
        while playing:
            try:
                x = pianobar.expect(pattern_list, timeout=0)
                if x == 0:
                    song = ''
                    artist = ''
                    album = ''

                    x = pianobar.expect(' \| ')
                    if x == 0:  # Title | Artist | Album
                        print('Song: "{}"'.format(pianobar.before))
                        song = pianobar.before
                        x = pianobar.expect(' \| ')
                        if x == 0:
                            print('Artist: "{}"'.format(pianobar.before))
                            artist = pianobar.before
                            x = pianobar.expect('\r\n')
                            if x == 0:
                                print('Album: "{}"'.format())
                                album = pianobar.before
                elif x == 1:
                    x = pianobar.expect(' \| ')
                    if x == 0:
                        print('Station: "{}"'.format(pianobar.before))
                elif x == 2:
                    # Time doesn't include newline - prints over itself.
                    x = pianobar.expect('\r', timeout=1)
                    if x == 0:
                        print('Time: {}'.format(pianobar.before))
                    # Periodically dump state (volume and station name)
                    # to pickle file so it's remembered between each run.
                    try:
                        pass
                        # f = open(PICKLEFILE, 'wb')
                        # pickle.dump([volCur, stationList[stationNum]], f)
                        # f.close()
                    except:
                        pass

                info_old = information
                information = [song, artist, album]
                if information != info_old:
                    get_album(song, artist, album)

            except pexpect.EOF:
                break
            except pexpect.TIMEOUT:
                break