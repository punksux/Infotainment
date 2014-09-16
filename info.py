from flask import Flask, request, render_template, url_for, redirect, Response
import logging
import logging.handlers
from socket import timeout
import json
from datetime import datetime, timedelta
import random
import time
from apscheduler.scheduler import Scheduler
import feedparser

weather_test = 100
on_pi = False
location = 84123
icon = ""
day = True
sun_or_moon_icon = ''
d_n_clouds = ''
rss_feed = 'http://www.kutv.com/news/features/top-stories/stories/rss.xml'
#rss_feed = 'http://rss.cnn.com/rss/cnn_topstories.rss'
feed = []

templateData = {
    'icon': ['', '', ''],
    'clouds':  '',
    'sun_moon': '',
    'precip': '',
    'sunset_hour': '2',
    'sunset_minute': '00',
    'background': '',
    'time': '',
    'day_night': 'day'
}

if on_pi:
    import urllib2
    #import RPi.GPIO as GPIO
    import socket
else:
    from urllib.request import urlopen
    import urllib.error

app = Flask(__name__)

#logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s',
                    #datefmt='%m/%d/%Y %I:%M:%S %p')

sched = Scheduler()
sched.start()


def get_rss():
    global feed
    feed = feedparser.parse(rss_feed)
    print(feed['items'][0]['title'])


get_rss()
rss = sched.add_interval_job(get_rss, seconds=5*60)


def check_weather():
    global icon
    global precip
    if weather_test == 200:
        global something_wrong
        global f
        weather_website = ('http://api.wunderground.com/api/c5e9d80d2269cb64/conditions/astronomy/q/%s.json' % location)
        if on_pi:
            try:
                f = urllib2.urlopen(weather_website, timeout=3)
                something_wrong = False
            except urllib2.URLError as e:
                logging.error('Data not retrieved because %s' % e)
                something_wrong = True
            except socket.timeout:
                logging.error('Socket timed out')
                something_wrong = True
        else:
            try:
                f = urlopen(weather_website, timeout=3)
                something_wrong = False
            except urllib.error.URLError as e:
                logging.error('Data not retrieved because %s' % e)
                something_wrong = True
            except timeout:
                logging.error('Socket timed out')
                something_wrong = True

        if something_wrong:
            logging.error("No Internet")
            templateData['temp'] = 0.0
        else:
            json_string = f.read()
            parsed_json = json.loads(json_string.decode("utf8"))
            icon = parsed_json['current_observation']['icon']
            print(icon)

            templateData['sunset_hour'] = parsed_json['sun_phase']['sunset']['hour']
            templateData['sunset_minute'] = parsed_json['sun_phase']['sunset']['minute']

            sun_or_moon()
            set_icon()
            f.close()
    else:
        #randt = ['rain', 'clear', 'partlycloudy', 'mostlycloudy', 'flurries']
        randt = ['rain', 'clear']
        icon = randt[random.randrange(0, 2)]
        sun_or_moon()
        set_icon()
        precip = True


def sun_or_moon():
    global day
    global sun_or_moon_icon
    global d_n_clouds
    sunset = datetime.now().replace(hour=int(templateData['sunset_hour']), minute=int(templateData['sunset_minute']),
                                    second=00, microsecond=0)

    if (sunset - datetime.now()).total_seconds() > 0:
        day = True
        sun_or_moon_icon = 'sun'
        d_n_clouds = 'day'
        templateData['background'] = '-moz-linear-gradient(top, #C9E3FB 0%, #529BE4 100%);'
        templateData['day_night'] = 'day'
    else:
        day = False
        sun_or_moon_icon = 'moon'
        d_n_clouds = 'night'
        templateData['background'] = '-moz-linear-gradient(top, #1f1f3f 0%, #141f31 100%);'
        templateData['day_night'] = 'night'


def set_icon():
    print(icon)
    filename = (icon.split("/")[len(icon.split("/"))-1]).replace('.gif', '')

    if filename == "clear" or filename == "sunny":
        templateData['icon'] = [sun_or_moon_icon, '', '', '']
    elif filename == "cloudy":
        templateData['icon'] = ['', 'clouds-back-' + d_n_clouds + '.png', 'cloud-' + d_n_clouds + '.png', '']
    elif filename == "flurries":
        templateData['icon'] = ['', 'clouds-back-' + d_n_clouds + '.png', 'cloud-' + d_n_clouds + '.png', 'flurries']
    elif filename == "fog":
        templateData['icon'] = ['', '', 'fog.png', '']
    elif filename == "hazy":
        templateData['icon'] = [sun_or_moon_icon, '', 'fog.png', '']
    elif filename == "mostlycloudy" or filename == 'partlysunny':
        templateData['icon'] = [sun_or_moon_icon, 'cloud-back-' + d_n_clouds + '.png', 'cloud-' + d_n_clouds + '.png', '']
    elif filename == "partlycloudy" or filename == 'mostlysunny':
        templateData['icon'] = [sun_or_moon_icon, '', 'cloud-' + d_n_clouds + '.png', '']
    elif filename == "sleet":
        templateData['icon'] = ['', 'clouds-' + d_n_clouds + '.png', 'sleet.png']
    elif filename == "rain":
        templateData['icon'] = ['', 'clouds-back-' + d_n_clouds + '.png', 'cloud-' + d_n_clouds + '.png', 'rain']


check_weather()
weather = sched.add_interval_job(check_weather, seconds=15)

def event_stream():
        yield 'event: outTemp\n' + \
              'data: ' + (str(random.randrange(-32, 104))) + '\n\n' + \
              'event: inTemp\n' + \
              'data: ' + str(random.randrange(32, 104)) + '\n\n' + \
              'event: time\n' + \
              'data: ' + str(datetime.now().time().strftime('%I:%M %p').lstrip("0")) + '\n\n' + \
              'event: rss1\n' + \
              'data: ' + feed['items'][0]['title'] + '\n\n' + \
              'event: rss1sum\n' + \
              'data: ' + feed['items'][0]['summary'] + '\n\n' + \
              'event: rss2\n' + \
              'data: ' + feed['items'][1]['title'] + '\n\n' + \
              'event: rss2sum\n' + \
              'data: ' + feed['items'][1]['summary'] + '\n\n' + \
              'event: rss3\n' + \
              'data: ' + feed['items'][2]['title'] + '\n\n' + \
              'event: rss3sum\n' + \
              'data: ' + feed['items'][2]['summary'] + '\n\n' + \
              'event: rss4\n' + \
              'data: ' + feed['items'][3]['title'] + '\n\n' + \
              'event: rss4sum\n' + \
              'data: ' + feed['items'][3]['summary'] + '\n\n' + \
              'event: rss5\n' + \
              'data: ' + feed['items'][4]['title'] + '\n\n' + \
              'event: rss5sum\n' + \
              'data: ' + feed['items'][4]['summary'] + '\n\n' + \
              'event: iconBack\n' + \
              'data: ' + templateData['icon'][0] + '\n\n' + \
              'event: iconMid\n' + \
              'data: ' + templateData['icon'][1] + '\n\n' + \
              'event: iconFront\n' + \
              'data: ' + templateData['icon'][2] + '\n\n' + \
              'event: precip\n' + \
              'data: ' + templateData['icon'][3] + '\n\n'

        time.sleep(0)


try:

    @app.route('/my_event_source')
    def sse_request():
        return Response(event_stream(), mimetype='text/event-stream')

    @app.route('/')
    def my_form():
        return render_template("index.html", **templateData)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80)

finally:
    sched.shutdown()