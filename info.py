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
#rss_feed = 'http://feeds.abcnews.com/abcnews/topstories'

weather_website = ('http://api.wunderground.com/api/c5e9d80d2269cb64/conditions/astronomy/forecast10day/q/%s.json' %
                   location)
feed = []
feed_titles = []
feed_titles_old = []
feed_summary = []
feed_summary_old = []
forecast_day = []
forecast_day_old = []
forecast_cond = []
forecast_cond_old = []
forecast_high = []
forecast_high_old = []
forecast_low = []
forecast_low_old = []
icon_old = []
tom_temp = '0'
tom_temp_old = '1'
day_night_old = ''
out_temp = '0'
out_temp_old = '0'
in_temp = '0'
in_temp_old = '0'

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


#    --==RSS Stuff==--
def get_rss():
    global feed, feed_titles, feed_summary, feed_titles_old, feed_summary_old
    feed = feedparser.parse(rss_feed)
    feed['items'] = feed['items'][:10]
    for i in feed['items']:
        feed_titles.append(i['title'])
        feed_summary.append(i['summary'])


get_rss()
rss = sched.add_interval_job(get_rss, seconds=5*60)


def check_weather():
    global icon, forecast_day, forecast_cond, forecast_high, forecast_low, forecast_day_old, forecast_cond_old
    global forecast_high_old, forecast_low_old, tom_temp
    if weather_test == 200:
        global something_wrong
        global f
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
            for i in range(0, 5):
                forecast_cond.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['icon'])
                forecast_day.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['date']['weekday'])
                forecast_high.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit'])
                forecast_low.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit'])

            tom_temp = parsed_json['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit']
            sun_or_moon()
            set_icon()
            f.close()
    else:
        def rand_weather():
            randt = ['rain', 'clear', 'partlycloudy', 'mostlycloudy', 'flurries']
            return randt[random.randrange(0, 5)]

        def get_rand():
            return random.randrange(60, 90)

        icon = rand_weather()
        sun_or_moon()

        tom_temp = get_rand()
        forecast_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        forecast_cond = [rand_weather(), rand_weather(), rand_weather(), rand_weather(), rand_weather()]
        forecast_high = [get_rand(), get_rand(), get_rand(), get_rand(), get_rand()]
        forecast_low = [get_rand(), get_rand(), get_rand(), get_rand(), get_rand()]

        # if templateData['day_night'] == 'day':
        #     templateData['day_night'] = 'night'
        # else:
        #     templateData['day_night'] = 'day'
        set_icon()


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
        #templateData['day_night'] = 'day'
    else:
        day = False
        sun_or_moon_icon = 'moon'
        d_n_clouds = 'night'
        templateData['background'] = '-moz-linear-gradient(top, #1f1f3f 0%, #141f31 100%);'
        #templateData['day_night'] = 'night'


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
        templateData['icon'] = [sun_or_moon_icon, 'cloud-back-' + d_n_clouds + '.png', 'cloud-' + d_n_clouds + '.png',
                                '']
    elif filename == "partlycloudy" or filename == 'mostlysunny':
        templateData['icon'] = [sun_or_moon_icon, '', 'cloud-' + d_n_clouds + '.png', '']
    elif filename == "sleet":
        templateData['icon'] = ['', 'clouds-' + d_n_clouds + '.png', 'sleet.png']
    elif filename == "rain":
        templateData['icon'] = ['', 'clouds-back-' + d_n_clouds + '.png', 'cloud-' + d_n_clouds + '.png', 'rain']


check_weather()
weather = sched.add_interval_job(check_weather, seconds=60)

rss_once = False


def get_temps_from_probes():
    global out_temp, in_temp
    out_temp = str(random.randrange(-32, 104))
    in_temp = str(random.randrange(32, 104))

get_temps_from_probes()
temps = sched.add_interval_job(get_temps_from_probes, seconds=10)

#     --==Streaming Stuff==--
def event_stream():
    global icon, forecast_day, forecast_cond, forecast_high, forecast_low, forecast_day_old, forecast_cond_old
    global forecast_high_old, forecast_low_old, icon_old, rss_once, feed_titles_old, feed_summary_old, tom_temp
    global tom_temp_old, day_night_old, out_temp_old, in_temp_old
    yield_me = ''
    if templateData['day_night'] != day_night_old:
        print(templateData['day_night'])
        day_night_old = templateData['day_night']
        yield_me += 'event: dayNight\n' + 'data: ' + templateData['day_night'] + '\n\n'
    if out_temp != out_temp_old:
        out_temp_old = out_temp
        yield_me += 'event: outTemp\n' + 'data: ' + str(out_temp) + '\n\n'
    if in_temp != in_temp_old:
        in_temp_old = in_temp
        yield_me += 'event: inTemp\n' + 'data: ' + str(in_temp) + '\n\n'
    if tom_temp != tom_temp_old:
        tom_temp_old = tom_temp
        yield_me += 'event: tomTemp\n' + 'data: ' + str(tom_temp) + '\n\n'
    if feed_titles != feed_titles_old or rss_once is False:
        feed_titles_old = feed_titles
        yield_me += 'event: rssTitle\n' + 'data: ' + json.dumps(feed_titles) + '\n\n'
    if feed_summary != feed_summary_old or rss_once is False:
        feed_summary_old = feed_summary
        rss_once = True
        yield_me += 'event: rssSum\n' + 'data: ' + json.dumps(feed_summary) + '\n\n'
    if templateData['icon'] != icon_old:
        icon_old = templateData['icon']
        yield_me += 'event: icon\n' + 'data: ' + json.dumps(templateData['icon']) + '\n\n'
    if forecast_day != forecast_day_old:
        forecast_day_old = forecast_day
        yield_me += 'event: forecastDay\n' + 'data: ' + json.dumps(forecast_day) + '\n\n'
    if forecast_cond != forecast_cond_old:
        forecast_cond_old = forecast_cond
        yield_me += 'event: forecastCond\n' + 'data: ' + json.dumps(forecast_cond) + '\n\n'
    if forecast_high != forecast_high_old:
        forecast_high_old = forecast_high
        yield_me += 'event: forecastHigh\n' + 'data: ' + json.dumps(forecast_high) + '\n\n'
    if forecast_low != forecast_low_old:
        forecast_low_old = forecast_low
        yield_me += 'event: forecastLow\n' + 'data: ' + json.dumps(forecast_low) + '\n\n'

    yield yield_me

    time.sleep(0)


try:

    @app.route('/my_event_source')
    def sse_request():
        return Response(event_stream(), mimetype='text/event-stream')

    @app.route('/')
    def my_form():
        global rss_once
        rss_once = False
        return render_template("index.html", **templateData)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80)

finally:
    sched.shutdown()