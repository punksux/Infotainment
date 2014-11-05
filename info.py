from flask import Flask, render_template, Response, request, jsonify
import logging
import logging.handlers
from socket import timeout
import json
from datetime import datetime, timedelta
import random
import time
from apscheduler.scheduler import Scheduler
import feedparser
import sports
import entertainment
import platform
import os
import re
import urllib
from urllib.request import Request, urlopen
import urllib.error
from urllib.parse import quote
from xml.etree import ElementTree as ET
import os.path
import requests

weather_test = True
on_pi = False
location = 84123
icon = ""
day = True

feed = []
rss_feed = []
rss_feed_old = []
forecast_day = []
forecast_day_old = []
forecast_cond = []
forecast_cond_old = []
forecast_high = []
forecast_high_old = []
forecast_low = []
forecast_low_old = []
forecast_decription = []
forecast_decription_old = []
icon_old = []
tom_temp = '0'
tom_temp_old = '1'
day_night = 'day'
day_night_old = ''
out_temp = '0'
out_temp_old = '0'
in_temp = '0'
in_temp_old = '0'
sunset_hour = 2
sunset_minute = 00
feed_source = ''
feed_source_old = ''
city_name = ''
observation_time = ''
current_cond = ''
allergy_forecast = []
predominant_pollen = ''
allergy_forecast_old = []
predominant_pollen_old = ''
full_weather = []
full_weather_old = []
hourly_temps = []
hourly_temps_old = []
alert = []
alert_old = []
utah_week = []
utah_week_old = []
utah_score_sched = None
sf_score_sched = None
kc_score_sched = None
soccer_score = None
utah_score_old = []
utah_score = []
sf_week = []
sf_week_old = []
kc_week = []
kc_week_old = []
sf_score = []
kc_score = []
sf_score_old = []
kc_score_old = []
rsl_week = []
rsl_week_old = []
rsl_score = []
rsl_score_old = []
ncaa_rankings = []
ncaa_rankings_old = []
pac12_standings = []
pac12_standings_old = []
soccer_standings = []
soccer_standings_old = []
nfl_rankings = []
nfl_rankings_old = []
opening_movies = []
opening_movies_old = []
local_events = []
local_events_old = []
album_info = []
album_info_old = []
stations = []
stations_old = []

#######  --== Set Platform ==--  #######
print("** Running on " + platform.uname()[0] + " **")
if platform.uname()[0] != 'Windows':
    on_pi = True

if on_pi:
    import psutil
    import pexpect


app = Flask(__name__)

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

sched = Scheduler()
sched.start()


#######  --== RSS Stuff ==--  #######
rss_feeds = ['http://www.kutv.com/news/features/top-stories/stories/rss.xml',
             'http://www.utahutes.com/sports/m-footbl/headline-rss.xml',
             'http://feeds.bbci.co.uk/news/technology/rss.xml',
             'http://rss.allrecipes.com/daily.aspx?hubID=80',
             'http://www.tmz.com/rss.xml']
rss_sources = ['KSL.com', 'UtahUtes.com', 'BBC Tech', 'AllRecipes', 'TMZ.com']

feed_no = 0


def get_rss():
    global feed, feed_no, rss_feed
    rss_feed = []
    feed = feedparser.parse(rss_feeds[feed_no])
    feed['items'] = feed['items'][:10]
    for i in feed['items']:
        rss_feed.append([i['title'].replace('#PrepareU: @Utah_Football', ''), i['summary']])
    rss_feed.append(rss_sources[feed_no])

    if feed_no == len(rss_feeds)-1:
        feed_no = 0
    else:
        feed_no += 1

#get_rss()
rss = sched.add_interval_job(get_rss, seconds=1*30)


#######  --== Weather Stuff ==--  #######
weather_website = ('http://api.wunderground.com/api/c5e9d80d2269cb64/conditions/astronomy/forecast10day/alerts/' +
                   'hourly/q/%s.json' % location)
allergy_website = 'http://www.claritin.com/weatherpollenservice/weatherpollenservice.svc/getforecast/84123'


def check_weather():
    global icon, forecast_day, forecast_cond, forecast_high, forecast_low, forecast_day_old, forecast_cond_old
    global forecast_high_old, forecast_low_old, tom_temp, sunset_hour, sunset_minute, day_night, city_name
    global observation_time, current_cond, predominant_pollen, allergy_forecast, full_weather, full_weather_old
    global sunrise_hour, sunrise_minute, relative_humidity, precip_today_string, wind_string, hourly_temps, alert
    global forecast_decription, forecast_decription_old
    if weather_test is False:
        global something_wrong
        global f, g
        try:
            f = urlopen(weather_website, timeout=3)
            req = Request(allergy_website, headers={'User-Agent': 'Mozilla/5.0'})
            g = urlopen(req, timeout=3)
            something_wrong = False
        except urllib.error.URLError as e:
            logging.error('Data not retrieved because - %s' % e)
            something_wrong = True
        except timeout:
            logging.error('Socket timed out')
            something_wrong = True

        if something_wrong:
            logging.error("No Internet")
        else:
            hourly_temps = []
            forecast_cond = []
            forecast_day = []
            forecast_high = []
            forecast_low = []
            forecast_decription = []

            json_string = f.read()
            parsed_json = json.loads(json_string.decode("utf8"))
            icon = parsed_json['current_observation']['icon']
            city_name = parsed_json['current_observation']['display_location']['full']
            observation_time = parsed_json['current_observation']['observation_time']
            current_cond = parsed_json['current_observation']['weather']
            relative_humidity = parsed_json['current_observation']['relative_humidity']
            precip_today_string = parsed_json['current_observation']['precip_today_string']
            wind_string = parsed_json['current_observation']['wind_string']

            sunset_hour = int(parsed_json['sun_phase']['sunset']['hour'])
            sunset_minute = int(parsed_json['sun_phase']['sunset']['minute'])
            sunrise_hour = int(parsed_json['sun_phase']['sunrise']['hour'])
            sunrise_minute = int(parsed_json['sun_phase']['sunrise']['minute'])

            for i in range(0, 12):
                hourly_temps.append(parsed_json['hourly_forecast'][i]['temp']['english'])

            j = 0
            for i in range(0, 5):
                forecast_cond.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['icon'])
                forecast_day.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['date']['weekday'])
                forecast_high.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit'])
                forecast_low.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit'])
                forecast_decription.append(parsed_json['forecast']['txt_forecast']['forecastday'][i+j]['fcttext'])
                j += 1
            tom_temp = parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']

            day_or_night()

            if parsed_json.get('alerts'):
                alert_description = parsed_json['alerts'][0]['description']
                alert_message = parsed_json['alerts'][0]['message']
                alert = [alert_description, alert_message]
            else:
                print('No Alert')

            f.close()

            json_string = g.read()
            parsed_json = json.loads(json_string.decode('utf-8'))
            set1 = parsed_json.find(':[')
            set2 = parsed_json.find('],')
            set3 = parsed_json.find('pp\":\"')
            set4 = parsed_json.find('\"time')
            predominant_pollen = parsed_json[set3+6: set4-2]
            allergy_forecast = parsed_json[set1+2: set2]
            allergy_forecast = str(allergy_forecast).split(",")
            g.close()

            full_weather = [city_name, observation_time, current_cond, sunset_hour, sunset_minute, sunrise_hour,
                            sunrise_minute, relative_humidity, precip_today_string, wind_string]

    else:  # Random test weather
        def rand_weather():
            randt = ['rain', 'clear', 'partlycloudy', 'mostlycloudy', 'flurries', 'snow', 'sunny', 'sleet',
                     'partlysunny', 'mostlysunny', 'tstorms', 'cloudy', 'fog', 'hazy', 'chancetstorms', 'chancerain',
                     'chancesnow', 'unknown']
            return randt[random.randrange(0, 18)]

        def rand_days():
            randt = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            return randt[random.randrange(0, 5)]

        def get_rand():
            return random.randrange(60, 90)

        icon = rand_weather()
        tom_temp = get_rand()
        forecast_day = [rand_days(), rand_days(), rand_days(), rand_days(), rand_days()]
        forecast_cond = [rand_weather(), rand_weather(), rand_weather(), rand_weather(), rand_weather()]
        forecast_high = [get_rand(), get_rand(), get_rand(), get_rand(), get_rand()]
        forecast_low = [get_rand(), get_rand(), get_rand(), get_rand(), get_rand()]
        forecast_decription = forecast_cond

        if day_night == 'day':
            day_night = 'night'
        else:
            day_night = 'day'

        def rand_allergy():
            return random.randrange(10, 120)/10

        allergy_forecast = [rand_allergy(), rand_allergy(), rand_allergy(), rand_allergy()]
        predominant_pollen = rand_weather()
        city_name = "Murray"
        observation_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        current_cond = icon
        sunset_hour = 22
        sunset_minute = 23
        sunrise_hour = 7
        sunrise_minute = 12
        relative_humidity = '32%'
        precip_today_string = '0.00 in'
        wind_string = 'Wind out of the East at 7MPH'
        full_weather = [city_name, observation_time, current_cond, sunset_hour, sunset_minute, sunrise_hour,
                        sunrise_minute, relative_humidity, precip_today_string, wind_string]
        hourly_temps = [get_rand(), get_rand(), get_rand(), get_rand(), get_rand(), get_rand(), get_rand(), get_rand(),
                        get_rand(), get_rand(), get_rand(), get_rand()]


def day_or_night():
    global day_night
    sunset = datetime.now().replace(hour=int(sunset_hour), minute=int(sunset_minute),
                                    second=00, microsecond=0)

    if (sunset - datetime.now()).total_seconds() > 0:
        day_night = 'day'
    else:
        day_night = 'night'

check_weather()
weather = sched.add_interval_job(check_weather, seconds=60)


#######  --== Get Temps ==--  #######
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temperature_file = '/sys/bus/w1/devices/28-0004749a3dff/w1_slave'


def get_temps_from_probes():
    global out_temp, in_temp
    if on_pi:
        y = open(temperature_file, 'r')
        lines = y.readlines()
        y.close()

        if lines[0].strip()[-3:] != 'YES':
            print('No temp from sensor.')
        else:
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                in_temp = temp_c * 9.0 / 5.0 + 32.0
                #print(in_temp)

        out_temp = str(random.randrange(-32, 104))

    else:
        out_temp = str(random.randrange(-32, 104))
        in_temp = str(random.randrange(32, 104))

get_temps_from_probes()
temps = sched.add_interval_job(get_temps_from_probes, seconds=30)


#######  --== Music Stuff ==--  #######
artist = ''
album = ''
song = ''
information = ['', '', '']
info_old = []
st = None
h = None
p = None
playing = False
st_got = False


def get_album(song2, artist2, album2, like2):
    try:
        global album_info
        last_fm_website = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&' \
                          'api_key=7e0ead667c3b37eb1ed9f3d16778fe38&artist=%s&album=%s&format=json' \
                          % (quote(artist2), quote(album2))
        chartlyrics_website = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?' \
                              'artist=%s&song=%s' % (quote(artist2), quote(song2))

        q = urlopen(last_fm_website)
        json_string = q.read()
        parsed_json = json.loads(json_string.decode('utf-8'))
        if 'image' in parsed_json['album']:
            album_art = parsed_json['album']['image'][3]['#text']
        else:
            album_art = '/static/images/pandora/blank.jpg'
        if 'wiki' in parsed_json['album']:
            album_sum = re.sub('<[^<]+?>', '', parsed_json['album']['wiki']['summary'])
        else:
            album_sum = ''

        try:
            t = ET.parse(chartlyrics_website)
            items = t.getroot()
            lyrics = items[9].text
            print(items)
        except:
            lyrics = ''

        album_info = [song2, artist2, album2, album_art, album_sum, like2, lyrics]
        print(album_info)
    except:
        album_info = [song2, artist2, album2, '/static/images/pandora/blank.jpg', '', like2, '']
        print(album_info)


def start_pianobar():
    global pianobar, h, playing, artist, album, song, information, info_old
    pianobar = pexpect.spawnu('sudo -u pi pianobar')

    playing = True
    #pattern_list = pianobar.compile_pattern_list(['SONG: ', 'STATION: ', 'TIME: '])
    print('Getting info')

    while pianobar.isalive():
        while playing:
            try:
                x = pianobar.expect('SONG: ', timeout=0)
                if x == 0:
                    song = ''
                    artist = ''
                    album = ''
                    like = ''

                    x = pianobar.expect(' \| ')
                    if x == 0:  # Title | Artist | Album
                        print('Song: "%s"' % pianobar.before)
                        song = pianobar.before
                        x = pianobar.expect(' \| ')
                        if x == 0:
                            print('Artist: "{}"'.format(pianobar.before))
                            artist = pianobar.before
                            x = pianobar.expect(' \| ')
                            if x == 0:
                                print('Album: "{}"'.format(pianobar.before))
                                album = pianobar.before
                                if re.search('\(', album) is not None:
                                    album = album[:re.search('\(', album).start()]
                                x = pianobar.expect('\r\n')
                                if x == 0:
                                    print('Like: "{}"'.format(pianobar.before))
                                    if pianobar.before == '<3':
                                        like = '1'
                                    else:
                                        like = '0'

                info_old = information
                information = [song, artist, album, like]
                if information != info_old:
                    get_album(song, artist, album, like)

                elif x == 1:
                    x = pianobar.expect(' \| ')
                    if x == 0:
                        print('Station: "{}"'.format(pianobar.before))
                elif x == 2:
                    # Time doesn't include newline - prints over itself.
                    x = pianobar.expect('\r', timeout=1)
                    if x == 0:
                        print('Time: {}'.format(pianobar.before))

            except pexpect.EOF:
                break
            except pexpect.TIMEOUT:
                break


def get_stations():
    global h, stations, st, st_got
    print('Getting stations')
    pianobar.sendcontrol('m')
    pianobar.expect('TIME: ', timeout=30)
    pianobar.send('s')
    try:
        pianobar.expect('Select station: ', timeout=10)
    except pexpect.TIMEOUT:
        print('Timed out - try again')
        get_stations()
    a = pianobar.before.splitlines()
    stations = []

    for b in a[:-1]:
        if (b.find('playlist...') >= 0) or (b.find('Autostart') >= 0) or (b.find('TIME:') >= 0):
            continue
        if b.find('Radio') or b.find('QuickMix'):
            id_no = b[5:7].strip()
            name = b[13:].strip()

            if name == 'QuickMix':
                stations.insert(0, [id_no, name])
            else:
                stations.append([id_no, name])
    pianobar.sendcontrol('m')
    st_got = True
    print(str(stations).replace('],', ']\n'))


def change_station_by_id(id_no):
    global pianobar
    print("Change to station #" + id_no)
    print('Clear out of any selection.')
    pianobar.sendcontrol('m')
    print('Wait for TIME:')
    pianobar.expect('TIME: ', timeout=30)
    print('Press s')
    pianobar.send('s')
    print('Wait for "Select station:"')
    try:
        pianobar.expect('Select station: ', timeout=30)
    except pexpect.TIMEOUT:
        print('Timed out - try again')
        change_station_by_id(id_no)
    print('Press ' + id_no)
    pianobar.send(id_no)
    print('Press enter')
    pianobar.sendcontrol('m')
    print('Changed')


#######  --== Entertainment Stuff ==--  #######
def get_opening_movies():
    global opening_movies
    opening_movies = entertainment.get_opening_movies()


def get_local_events():
    global local_events
    local_events = entertainment.get_local_events()

get_opening_movies()
get_local_events()


####### --==Sports Stuff==-- #######
ncaa_team_names = {'ORS': 'Oregon State', 'ASU': 'Arizona State', 'ORE': 'Oregon', 'STA': 'Stanford', 'ARI': 'Arizona',
                   'COL': 'Colorado', 'UTH': 'Utah'}
nfl_team_names = {'SF': 'San Francisco', 'KC': 'Kansas City', 'DAL': 'Dallas', 'CHI': 'Chicago', 'ARI': 'Arizona',
                  'PHI': 'Philidelphia', 'STL': 'St. Louis', 'DEN': 'Denver', 'NO': 'New Orleans', 'NYG': 'New York',
                  'WAS': 'Washington', 'SEA': 'Seattle', 'OAK': 'Oakland', 'SD': 'San Diego'}


def football_weekly(week, team):
    global utah_week, sf_week, kc_week, ncaa_rankings, pac12_standings, nfl_rankings, nfl_rank_checked
    week_sched = sports.get_weekly_schedule(week, team)
    #game = sched.add_date_job(start_football_scores, datetime.strptime(week_sched[3], '%Y-%m-%d %H:%M:%S'),
                              #args=[week_sched[0], week_sched[1], week_sched[2]])

    nfl_rank_checked = False
    if week_sched[2] != 'BYE':
        week_sched[3] = datetime.strptime(week_sched[3], '%Y-%m-%d %H:%M:%S').strftime('%a %b %d<br />%I:%M %p')
    if team == 'UTH':
        ncaa_rankings = sports.get_ncaa_rankings(week)
        pac12_standings = sports.get_ncaa_standings()
        utah_week = week_sched
        for k, v in ncaa_team_names.items():
            utah_week[1] = utah_week[1].replace(k, v)
            utah_week[2] = utah_week[2].replace(k, v)
    elif team == 'SF':
        nfl_rankings = sports.get_nfl_rankings()
        nfl_rank_checked = True
        sf_week = week_sched
        for k, v in nfl_team_names.items():
            sf_week[1] = sf_week[1].replace(k, v)
            sf_week[2] = sf_week[2].replace(k, v)
    elif team == 'KC':
        if nfl_rank_checked is False:
            nfl_rankings = sports.get_nfl_rankings()
        kc_week = week_sched
        for k, v in nfl_team_names.items():
            kc_week[1] = kc_week[1].replace(k, v)
            kc_week[2] = kc_week[2].replace(k, v)


def start_football_scores(week, home, away):
    global utah_score_sched, sf_score_sched, kc_score_sched
    if home == 'UTH' or away == 'UTH':
        utah_score_sched = sched.add_interval_job(football_scores, args=[week, home, away], seconds=30*60)
    elif home == 'SF' or away == 'SF':
        sf_score_sched = sched.add_interval_job(football_scores, args=[week, home, away], seconds=30*60)
    elif home == 'KC' or away == 'KC':
        kc_score_sched = sched.add_interval_job(football_scores, args=[week, home, away], seconds=30*60)


def football_scores(week, home, away):
    global utah_score, sf_score, kc_score, next_game
    football_score = sports.get_boxscore(week, home, away)

    if home == 'UTH' or away == 'UTH':
        utah_score = football_score
    elif home == 'SF' or away == 'SF':
        sf_score = football_score
    elif home == 'KC' or away == 'KC':
        kc_score = football_score

    if utah_score[0] == 'complete':
        sched.unschedule_job(utah_score_sched)
        next_game = sched.add_date_job(football_weekly, datetime.now().replace(day=datetime.now().day+2, hour=0,
                                                                               minute=1, second=0, microsecond=00),
                                       args={(int(week)+1), 'UTH'})
    elif sf_score[0] == 'complete':
        sched.unschedule_job(sf_score_sched)
        next_game = sched.add_date_job(football_weekly, datetime.now().replace(day=datetime.now().day+2, hour=0,
                                                                               minute=1, second=0, microsecond=00),
                                       args={(int(week)+1), 'SF'})
    elif kc_score[0] == 'complete':
        sched.unschedule_job(kc_score_sched)
        next_game = sched.add_date_job(football_weekly, datetime.now().replace(day=datetime.now().day+2, hour=0,
                                                                               minute=1, second=0, microsecond=00),
                                       args={(int(week)+1), 'KC'})


def football_season():
    teams = ['UTH', 'SF', 'KC']
    for t in teams:
        schedule = sports.get_season_schedule(t)
        for i in schedule:
            if (datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S') - datetime.now()).total_seconds() > 0:
                football_weekly(i[0], t)
                break

football_season()


def soccer_scores(game_id):
    global rsl_score, soccer_next_game
    rsl_score = sports.soccer_scores(game_id)
    if rsl_score[4] == 'complete':
        sched.unschedule_job(soccer_score)
        soccer_next_game = sched.add_date_job(soccer_season, datetime.now().replace(day=datetime.now().day+2, hour=0,
                                                                                    minute=1, second=0, microsecond=00))


def soccer_season():
    global rsl_week, soccer_score, soccer_standings
    schedule = sports.get_soccer_season()
    soccer_standings = sports.get_soccer_standings()
    for i in schedule:
            if (datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S') - datetime.now()).total_seconds() > 0:
                rsl_week = i
                soccer_score = sched.add_interval_job(soccer_scores, seconds=30*60,
                                                      start_date=datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S'),
                                                      args=i[0])
                rsl_week[3] = datetime.strptime(rsl_week[3], '%Y-%m-%d %H:%M:%S').strftime('%a %b %d<br />%I:%M %p')
                break

soccer_season()
#sched.print_jobs()

test = False


#######  --==Streaming Stuff==--  #######
def event_stream():
    global icon, forecast_day_old, forecast_cond_old, test, forecast_high_old, forecast_low_old, icon_old,\
        tom_temp, tom_temp_old, day_night_old, out_temp_old, in_temp_old,\
        allergy_forecast_old, predominant_pollen_old,  full_weather_old, hourly_temps_old, alert_old,\
        utah_week_old, utah_score_old, sf_week_old, kc_week_old, sf_score_old, kc_score_old, rsl_week_old,\
        rsl_score_old, ncaa_rankings_old, pac12_standings_old, soccer_standings_old, nfl_rankings_old,\
        opening_movies_old, local_events_old, forecast_decription, forecast_decription_old,\
        album_info_old, stations, stations_old, st_got, rss_feed_old

    yield_me = ''
    if day_night != day_night_old or test is False:
        day_night_old = day_night
        yield_me += 'event: dayNight\n' + 'data: ' + day_night + '\n\n'
    if out_temp != out_temp_old or test is False:
        out_temp_old = out_temp
        yield_me += 'event: outTemp\n' + 'data: ' + str(out_temp) + '\n\n'
    if in_temp != in_temp_old or test is False:
        in_temp_old = in_temp
        yield_me += 'event: inTemp\n' + 'data: ' + str(in_temp) + '\n\n'
    if tom_temp != tom_temp_old or test is False:
        tom_temp_old = tom_temp
        yield_me += 'event: tomTemp\n' + 'data: ' + str(tom_temp) + '\n\n'
    if rss_feed != rss_feed_old or test is False:
        rss_feed_old = rss_feed
        yield_me += 'event: rssFeed\n' + 'data: ' + json.dumps(rss_feed) + '\n\n'
    if icon != icon_old or test is False:
        icon_old = icon
        yield_me += 'event: icon\n' + 'data: ' + icon + '\n\n'
    if forecast_day != forecast_day_old or test is False:
        forecast_day_old = forecast_day
        yield_me += 'event: forecastDay\n' + 'data: ' + json.dumps(forecast_day) + '\n\n'
    if forecast_cond != forecast_cond_old or test is False:
        forecast_cond_old = forecast_cond
        yield_me += 'event: forecastCond\n' + 'data: ' + json.dumps(forecast_cond) + '\n\n'
    if forecast_high != forecast_high_old or test is False:
        forecast_high_old = forecast_high
        yield_me += 'event: forecastHigh\n' + 'data: ' + json.dumps(forecast_high) + '\n\n'
    if forecast_low != forecast_low_old or test is False:
        forecast_low_old = forecast_low
        yield_me += 'event: forecastLow\n' + 'data: ' + json.dumps(forecast_low) + '\n\n'
    if forecast_decription != forecast_decription_old or test is False:
        forecast_decription_old = forecast_decription
        yield_me += 'event: forecastDecription\n' + 'data: ' + json.dumps(forecast_decription) + '\n\n'
    if allergy_forecast != allergy_forecast_old or test is False:
        allergy_forecast_old = allergy_forecast
        yield_me += 'event: allergyForecast\n' + 'data: ' + json.dumps(allergy_forecast) + '\n\n'
    if predominant_pollen != predominant_pollen_old or test is False:
        predominant_pollen_old = predominant_pollen
        yield_me += 'event: predominantPollen\n' + 'data: ' + predominant_pollen + '\n\n'
    if full_weather != full_weather_old or test is False:
        full_weather_old = full_weather
        yield_me += 'event: fullWeather\n' + 'data: ' + json.dumps(full_weather) + '\n\n'
    if hourly_temps != hourly_temps_old or test is False:
        hourly_temps_old = hourly_temps
        yield_me += 'event: hourlyTemps\n' + 'data: ' + json.dumps(hourly_temps) + '\n\n'
    if alert != alert_old or test is False:
        alert_old = alert
        yield_me += 'event: alert\n' + 'data: ' + json.dumps(alert) + '\n\n'
    if utah_week != utah_week_old or test is False:
        utah_week_old = utah_week
        yield_me += 'event: utahInfo\n' + 'data: ' + json.dumps(utah_week) + '\n\n'
    if utah_score != utah_score_old:
        utah_score_old = utah_score
        yield_me += 'event: utahScore\n' + 'data: ' + json.dumps(utah_score) + '\n\n'
    if sf_week != sf_week_old or test is False:
        sf_week_old = sf_week
        yield_me += 'event: sfInfo\n' + 'data: ' + json.dumps(sf_week) + '\n\n'
    if sf_score != sf_score_old:
        sf_score_old = sf_score
        yield_me += 'event: sfScore\n' + 'data: ' + json.dumps(sf_score) + '\n\n'
    if kc_week != kc_week_old or test is False:
        kc_week_old = kc_week
        yield_me += 'event: kcInfo\n' + 'data: ' + json.dumps(kc_week) + '\n\n'
    if kc_score != kc_score_old:
        kc_score_old = kc_score
        yield_me += 'event: kcScore\n' + 'data: ' + json.dumps(kc_score) + '\n\n'
    if rsl_week != rsl_week_old or test is False:
        rsl_week_old = rsl_week
        yield_me += 'event: rslInfo\n' + 'data: ' + json.dumps(rsl_week) + '\n\n'
    if rsl_score != rsl_score_old:
        rsl_score_old = rsl_score
        yield_me += 'event: rslScore\n' + 'data: ' + json.dumps(rsl_score) + '\n\n'
    if ncaa_rankings != ncaa_rankings_old or test is False:
        ncaa_rankings_old = ncaa_rankings
        yield_me += 'event: ncaaRankings\n' + 'data: ' + json.dumps(ncaa_rankings) + '\n\n'
    if pac12_standings != pac12_standings_old or test is False:
        pac12_standings_old = pac12_standings
        yield_me += 'event: pac12Standings\n' + 'data: ' + json.dumps(pac12_standings) + '\n\n'
    if soccer_standings != soccer_standings_old or test is False:
        soccer_standings_old = soccer_standings
        yield_me += 'event: soccerStandings\n' + 'data: ' + json.dumps(soccer_standings) + '\n\n'
    if nfl_rankings != nfl_rankings_old or test is False:
        nfl_rankings_old = nfl_rankings
        yield_me += 'event: nflRankings\n' + 'data: ' + json.dumps(nfl_rankings) + '\n\n'
    if opening_movies != opening_movies_old or test is False:
        opening_movies_old = opening_movies
        yield_me += 'event: openingMovies\n' + 'data: ' + json.dumps(opening_movies) + '\n\n'
    if local_events != local_events_old or test is False:
        local_events_old = local_events
        yield_me += 'event: localEvents\n' + 'data: ' + json.dumps(local_events) + '\n\n'
    if album_info != album_info_old or test is False:
        album_info_old = album_info
        test = True
        yield_me += 'event: albumInfo\n' + 'data: ' + json.dumps(album_info) + '\n\n'
    if st_got:
        st_got = False
        yield_me += 'event: stations\n' + 'data: ' + json.dumps(stations) + '\n\n'

    yield yield_me

    time.sleep(0)

print('OK GO')

try:

    @app.route('/my_event_source')
    def sse_request():
        return Response(event_stream(), mimetype='text/event-stream')

    @app.route('/')
    def my_form():
        global test, st_got
        test = False
        st_got = True
        return render_template("index.html")

    @app.route('/entertainment', methods=['POST'])
    def send_to_phone():
        a = request.form.get('a', 'something is wrong', type=str)
        b = request.form.get('b', 'something is wrong', type=str)
        print(a + ' - ' + b)
        data = dict(title=a, url=b, type='link')
        api_key = 'v1DxHg2oyCZCPc5Xr6KiVh4X3sLfkdibX2ujBvxC0RbUW'
        requests.post('https://api.pushbullet.com/v2/pushes', auth=(api_key, ''), data=data)
        return jsonify({'1': ''})

    @app.route('/music', methods=['POST'])
    def music_control():
        global pianobar, h, st
        button = request.form.get('button', 'something is wrong', type=str)
        print(button + ' button pressed')
        if on_pi:
            if button == 'P':
                for proc in psutil.process_iter():
                    if 'pianobar' in proc.name():
                        print('pianobar running')
                        pianobar.send(button)
                        break
                else:
                    print('starting pianobar')
                    h = sched.add_date_job(start_pianobar, (datetime.now() + timedelta(seconds=2)))
                    st = sched.add_date_job(get_stations, (datetime.now() + timedelta(seconds=20)))
            else:
                pianobar.send(button)
        else:
            pianobar.send(button)
        return jsonify({'1': ''})

    @app.route('/stationSelect', methods=['POST'])
    def change_station():
        global h
        id_no = request.form.get('id', 'something is wrong', type=str)
        h = sched.add_date_job(change_station_by_id, (datetime.now() + timedelta(seconds=2)), args=id_no)
        return jsonify({'1': ''})

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=88)

finally:
    print('Shutting Down!')
    playing = False
    print('Killing pianobar')
    pianobar.sendline('q')
    for proc in psutil.process_iter():
        if 'pianobar' in proc.name():
            print('Didn\'t kill, killing harder - pid ' + str(proc.pid))
            os.system('sudo kill ' + proc.pid)
    print('Shutting down scheduler')
    sched.shutdown(wait=False)
    print('Clear errors log')
    f = open('errors.log', 'w')
    f.close()
    print('Done')