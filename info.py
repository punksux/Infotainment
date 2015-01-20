from flask import Flask, render_template, Response, request, jsonify
import logging
import logging.handlers
from socket import timeout
import json
from datetime import datetime, timedelta
import random
import time
from apscheduler.scheduler import Scheduler
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
import news
from operator import itemgetter
import requests

weather_test = True
on_pi = False
location = 84123
icon = ""
day = True

day_night = 'day'
day_night_old = ''
full_weather = []
current_rain = ''
yield_me = ''


#######  --== Set Platform ==--  #######
print("** Running on " + platform.uname()[0] + " **")
if platform.uname()[0] != 'Windows':
    on_pi = True

if on_pi:
    import psutil
    import pexpect
    weather_test = False


app = Flask(__name__)

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

sched = Scheduler()
sched.start()


#######  --== Write Streaming Stuff ==--  #######
def write_yield(event, data):
    global yield_me
    if type(data) is list:
        data = json.dumps(data)

    yield_me += 'event: ' + event + '\n' + 'data: ' + str(data) + '\n\n'


#######  --== RSS Stuff ==--  #######
def get_rss():
    write_yield('rssFeed', news.get_news())

get_rss()
rss = sched.add_interval_job(get_rss, seconds=60 * 60)


#######  --== Weather Stuff ==--  #######
weather_website = ('http://api.wunderground.com/api/c5e9d80d2269cb64/conditions/astronomy/forecast10day/alerts/' +
                   'hourly/q/%s.json' % location)
allergy_website = 'http://www.claritin.com/weatherpollenservice/weatherpollenservice.svc/getforecast/84123'


def check_weather():
    global icon, day_night, current_rain, full_weather
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
            f.close()
            parsed_json = json.loads(json_string.decode("utf8"))
            icon = parsed_json['current_observation']['icon']
            city_name = parsed_json['current_observation']['display_location']['full']
            observation_time = parsed_json['current_observation']['observation_time']
            current_cond = parsed_json['current_observation']['weather']
            relative_humidity = parsed_json['current_observation']['relative_humidity']
            precip_today_string = parsed_json['current_observation']['precip_today_string']
            wind_string = parsed_json['current_observation']['wind_string']
            current_rain = parsed_json['current_observation']['precip_today_in']

            sunset_hour = int(parsed_json['sun_phase']['sunset']['hour'])
            sunset_minute = int(parsed_json['sun_phase']['sunset']['minute'])
            sunrise_hour = int(parsed_json['sun_phase']['sunrise']['hour'])
            sunrise_minute = int(parsed_json['sun_phase']['sunrise']['minute'])
            day_or_night(sunset_hour, sunset_minute)
            write_yield('dayNight', day_night)

            for i in range(0, 12):
                hourly_temps.append(parsed_json['hourly_forecast'][i]['temp']['english'])
            write_yield('hourlyTemps', hourly_temps)

            j = 0
            for i in range(0, 5):
                forecast_cond.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['icon'])
                forecast_day.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['date']['weekday'])
                forecast_high.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit'])
                forecast_low.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit'])
                forecast_decription.append(parsed_json['forecast']['txt_forecast']['forecastday'][i + j]['fcttext'])
                j += 1

            write_yield('forecastCond', forecast_cond)
            write_yield('forecastDay', forecast_day)
            write_yield('forecastHigh', forecast_high)
            write_yield('forecastLow', forecast_low)
            write_yield('forecastDecription', forecast_decription)

            write_yield('tomTemp', parsed_json['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit'])

            icon_image(icon)

            if parsed_json.get('alerts'):
                alert_description = parsed_json['alerts'][0]['description']
                alert_message = parsed_json['alerts'][0]['message']
                write_yield('alert', [alert_description, alert_message])
            else:
                write_yield('alert', ['', ''])

            json_string = g.read()
            g.close()
            parsed_json = json.loads(json_string.decode('utf-8'))
            set1 = parsed_json.find(':[')
            set2 = parsed_json.find('],')
            set3 = parsed_json.find('"pp')
            set4 = parsed_json.find('"timestamp')
            write_yield('predominantPollen', parsed_json[set3 + 6: set4 - 3])
            allergy_forecast = parsed_json[set1 + 2: set2]
            write_yield('allergyForecast', str(allergy_forecast).split(","))

            full_weather = [city_name, observation_time, current_cond, sunset_hour, sunset_minute, sunrise_hour,
                            sunrise_minute, relative_humidity, precip_today_string, wind_string]
            write_yield('fullWeather', full_weather)

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
        write_yield('tomTemp', get_rand())
        write_yield('forecastDay', [rand_days(), rand_days(), rand_days(), rand_days(), rand_days()])
        forecast_cond = [rand_weather(), rand_weather(), rand_weather(), rand_weather(), rand_weather()]
        write_yield('forecastCond', forecast_cond)
        write_yield('forecastHigh', [get_rand(), get_rand(), get_rand(), get_rand(), get_rand()])
        write_yield('forecastLow', [get_rand(), get_rand(), get_rand(), get_rand(), get_rand()])
        write_yield('forecastDecription', forecast_cond)

        if day_night == 'day':
            day_night = 'night'
        else:
            day_night = 'day'

        write_yield('dayNight', day_night)

        def rand_allergy():
            return random.randrange(10, 120) / 10

        write_yield('allergyForecast', [rand_allergy(), rand_allergy(), rand_allergy(), rand_allergy()])
        write_yield('predominantPollen', rand_weather())
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
        write_yield('fullWeather', full_weather)
        write_yield('hourlyTemps', [get_rand(), get_rand(), get_rand(), get_rand(), get_rand(), get_rand(), get_rand(),
                                    get_rand(), get_rand(), get_rand(), get_rand(), get_rand()])

        icon_image(icon)
        write_yield('alert', ['', ''])


def icon_image(icon_name):
    global icon
    if icon_name == 'partlysunny':
        icon_name = 'mostlycloudy'
    elif icon_name == 'mostlysunny':
        icon_name = 'partlycloudy'
    elif icon_name == 'sunny':
        icon_name = 'clear'
    elif icon_name[0:6] == 'chance':
        icon_name = icon_name[6:]
    else:
        icon_name = icon_name

    rand = random.randint(1, 5)
    fname = 'static/images/bg/' + day_night + '-' + icon_name + '-' + str(rand) + '.jpg'

    if os.path.exists(fname):
        write_yield('icon', fname)
    else:
        icon_image(icon_name)


def day_or_night(sh, sm):
    global day_night
    sunset = datetime.now().replace(hour=int(sh), minute=int(sm),
                                    second=00, microsecond=0)

    if (sunset - datetime.now()).total_seconds() > 0:
        day_night = 'day'
    else:
        day_night = 'night'

check_weather()
dt = datetime.now()
if on_pi:
    if dt.minute > 30:
        weather = sched.add_interval_job(check_weather, seconds=30 * 60, start_date=((dt + timedelta(hours=1)).replace(minute=0, second=0)))
    else:
        weather = sched.add_interval_job(check_weather, seconds=30 * 60, start_date=(dt.replace(minute=30, second=0)))
else:
    weather = sched.add_interval_job(check_weather, seconds=60)


#######  --== Get Temps ==--  #######
if on_pi:
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    temperature_file = '/sys/bus/w1/devices/28-0004749a3dff/w1_slave'


def get_temps_from_probes():
    global in_temp
    if on_pi:
        y = open(temperature_file, 'r')
        lines = y.readlines()
        y.close()

        if lines[0].strip()[-3:] != 'YES':
            print('No temp from sensor.')
        else:
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos + 2:]
                temp_c = float(temp_string) / 1000.0
                in_temp = temp_c * 9.0 / 5.0 + 32.0
                write_yield('inTemp', in_temp)
                #print(in_temp)

        write_yield('outTemp', str(random.randrange(-32, 104)))

    else:
        write_yield('outTemp', str(random.randrange(-32, 104)))
        write_yield('inTemp', str(random.randrange(32, 104)))

get_temps_from_probes()
temps = sched.add_interval_job(get_temps_from_probes, seconds=15)


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
            print('Getting lyrics')
            t = ET.parse(urlopen(chartlyrics_website))
            items = t.getroot()
            lyrics = items[9].text.replace('\n', '<br />')
            if lyrics is None:
                lyrics = ''
        except:
            lyrics = ''

        album_info = [song2, artist2, album2, album_art, album_sum, like2, lyrics]
        write_yield('albumInfo', album_info)
        print(album_info)
    except:
        album_info = [song2, artist2, album2, '/static/images/pandora/blank.jpg', '', like2, '']
        print(album_info)
        write_yield('albumInfo', album_info)


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

                # elif x == 1:
                #     x = pianobar.expect(' \| ')
                #     if x == 0:
                #         print('Station: "{}"'.format(pianobar.before))
                # elif x == 2:
                #     # Time doesn't include newline - prints over itself.
                #     x = pianobar.expect('\r', timeout=1)
                #     if x == 0:
                #         print('Time: {}'.format(pianobar.before))

            except pexpect.EOF:
                break
            except pexpect.TIMEOUT:
                break


def get_stations():
    global h, stations, st, st_got
    print('Getting stations')
    pianobar.sendcontrol('m')
    try:
        pianobar.expect('TIME: ', timeout=30)
        pianobar.sendline('s')
        try:
            pianobar.expect('Select station: ', timeout=30)
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
            write_yield('stations', stations)

        except pexpect.TIMEOUT:
            get_stations()
    except pexpect.TIMEOUT:
            get_stations()


def change_station_by_id(id_no):
    global pianobar
    print("Change to station #" + id_no)
    print('Clear out of any selection.')
    pianobar.sendcontrol('m')
    print('Press s')
    pianobar.send('s')
    print('Wait for "Select station:"')
    try:
        pianobar.expect('Select station: ', timeout=30)
        print('Press ' + id_no)
        pianobar.send(id_no)
        print('Press enter')
        pianobar.sendcontrol('m')
        print('Changed')
    except pexpect.TIMEOUT:
        print('Timed out - try again')
        change_station_by_id(id_no)


#######  --== Entertainment Stuff ==--  #######
def get_opening_movies():
    write_yield('openingMovies', entertainment.get_opening_movies())


def get_local_events():
    write_yield('localEvents', entertainment.get_local_events())

get_opening_movies()
dt = datetime.now()
movies = sched.add_interval_job(get_opening_movies, days=7, start_date=(dt + timedelta(days=7) - timedelta(days=dt.weekday() - 1)).replace(hour=0, minute=2, second=0))
get_local_events()
events = sched.add_interval_job(get_local_events, days=1, start_date=(dt + timedelta(days=1)).replace(hour=0, minute=2, second=0))


def get_jeopardy():
    write_yield('jeopardy', entertainment.jeopardy())

# get_jeopardy()
jeopardy = sched.add_interval_job(get_jeopardy, seconds=60 * 60, start_date=(dt + timedelta(hours=1)).replace(minute=10, second=0))


def get_cheezburger():
    get = entertainment.cheezburger()
    if get != '':
        write_yield('cheezburger', get)

# get_cheezburger()
cheezburger = sched.add_interval_job(get_cheezburger, seconds=random.randint(45, 90) * 60, start_date=(dt + timedelta(hours=1)).replace(minute=15, second=0))


def get_flickr():
    write_yield('flickr', entertainment.flickr())

get_flickr()
flickr = sched.add_interval_job(get_flickr, seconds=random.randint(45, 90) * 60, start_date=(dt + timedelta(hours=1)).replace(minute=45, second=0))


def get_facts():
    get = entertainment.sotruefacts()
    if get != '':
        write_yield('facts', get)

# get_facts()
facts = sched.add_interval_job(get_facts, seconds=random.randint(45, 90) * 60, start_date=(dt + timedelta(hours=1)).replace(minute=55, second=0))

#######  --==Holiday Stuff==--  #######
holidays = ["New Year\u2019s Day", "Groundhog Day", "Valentine\u2019s Day", "Washington\u2019s Birthday",
            "Saint Patrick\u2019s Day", "April Fools\u2019 Day", "Earth Day", "Star Wars Day", "Cinco de Mayo",
            "Mother\u2019s Day", "Memorial Day", "Flag Day", "Father\u2019s Day", "Independence Day", "Labor Day",
            "Halloween", "Veterans Day", "Thanksgiving Day", "Christmas", "New Year\u2019s Eve", "Easter"]
like_holiday = ["Saint Patrick\u2019s Day", "Halloween", "Thanksgiving Day", "Christmas"]
holiday_list = []


def get_holidays():
    global holiday_list
    holiday_website = 'http://holidayapi.com/v1/holidays?country=US&year=%s' % datetime.now().year
    w = urlopen(holiday_website)
    json_string = w.read()
    parsed_json = json.loads(json_string.decode('utf-8'))
    for i in parsed_json['holidays']:
        for j in parsed_json['holidays'][i]:
            if j['name'] in holidays:
                holiday_list.append([j['date'], j['name']])

    holiday_list = sorted(holiday_list, key=itemgetter(0))


get_holidays()
holiday_sched = sched.add_interval_job(get_holidays, days=365, start_date=datetime.now()
                                       .replace(year=datetime.now().year + 1, month=1, day=1, hour=0, minute=5))


def check_holiday():
    for i in holiday_list:
        da = datetime.strptime(i[0], '%Y-%m-%d')
        if (da - datetime.now()).total_seconds() > 0:
            if i[1] in like_holiday:
                if (da - datetime.now()).days < 14:
                    write_yield('holiday', i)
                else:
                    holiday_day = sched.add_date_job(run_holiday, da - timedelta(days=-14).replace(hour=0, minute=1, second=0), args=i)
                break
            else:
                if (da - datetime.now()).days < 3:
                    write_yield('holiday', i)
                else:
                    holiday_day = sched.add_date_job(run_holiday, (da - timedelta(days=-3)).replace(hour=0, minute=1, second=0), args=i)
                break
    else:
        pass


def run_holiday(hday):
    write_yield('holiday', hday)


check_holiday()
holiday_day_sched = sched.add_interval_job(check_holiday, days=1, start_date=(datetime.now() + timedelta(days=1)).replace(hour=0, minute=2))


#sched.print_jobs()
print('OK GO')
temp_yield = yield_me

#######  --==Web Part==--  #######
try:
    @app.route('/my_event_source')
    def sse_request():
        global yield_me
        temp = yield_me
        yield_me = ''
        return Response(temp, mimetype='text/event-stream')

    @app.route('/')
    def my_form():
        global yield_me
        yield_me = temp_yield
        return render_template("index.html")

    @app.route('/entertainment', methods=['POST'])
    def send_to_phone():
        a = request.form.get('a', 'something is wrong', type=str)
        b = request.form.get('b', 'something is wrong', type=str)
        print(a + ' - ' + b)
        if on_pi:
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

    @app.route('/weather.json', methods=['GET'])
    def give_weather():
        return jsonify({'weather': full_weather[2], 'ssHour': full_weather[3], 'ssMinute': full_weather[4],
                        'rain': current_rain})

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=88)

finally:
    print('Shutting Down!')
    playing = False
    print('Killing pianobar')
    try:
        pianobar.sendline('q')
    except:
        pass
    for procs in psutil.process_iter():
        if 'pianobar' in procs.name():
            print('Didn\'t kill, killing harder - pid ' + str(procs.pid))
            os.system('sudo kill ' + str(procs.pid))
    print('Shutting down scheduler')
    sched.shutdown(wait=False)
    print('Clear errors log')
    f = open('errors.log', 'w')
    f.close()
    print('Done')