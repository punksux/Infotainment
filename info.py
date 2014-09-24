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
day_night = 'day'
day_night_old = ''
out_temp = '0'
out_temp_old = '0'
in_temp = '0'
in_temp_old = '0'
sunset_hour = 2
sunset_minute = 00

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
    global forecast_high_old, forecast_low_old, tom_temp, sunset_hour, sunset_minute, day_night
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
        else:
            json_string = f.read()
            parsed_json = json.loads(json_string.decode("utf8"))

            icon = parsed_json['current_observation']['icon']
            sunset_hour = int(parsed_json['sun_phase']['sunset']['hour'])
            sunset_minute = int(parsed_json['sun_phase']['sunset']['minute'])
            for i in range(0, 5):
                forecast_cond.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['icon'])
                forecast_day.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['date']['weekday'])
                forecast_high.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit'])
                forecast_low.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit'])

            tom_temp = parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
            day_or_night()
            f.close()
    else:
        def rand_weather():
            randt = ['rain', 'clear', 'partlycloudy', 'mostlycloudy', 'flurries', 'snow', 'sunny', 'sleet',
                     'partlysunny', 'mostlysunny', 'tstorms', 'cloudy', 'fog', 'hazy']
            return randt[random.randrange(0, 14)]

        def rand_days():
            randt = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            return randt[random.randrange(0, 5)]

        def get_rand():
            return random.randrange(60, 90)

        icon = rand_weather()
        #day_or_night()

        tom_temp = get_rand()
        forecast_day = [rand_days(), rand_days(), rand_days(), rand_days(), rand_days()]
        forecast_cond = [rand_weather(), rand_weather(), rand_weather(), rand_weather(), rand_weather()]
        forecast_high = [get_rand(), get_rand(), get_rand(), get_rand(), get_rand()]
        forecast_low = [get_rand(), get_rand(), get_rand(), get_rand(), get_rand()]

        if day_night == 'day':
            day_night = 'night'
        else:
            day_night = 'day'


def day_or_night():
    global day_night
    global sun_or_moon_icon
    sunset = datetime.now().replace(hour=int(sunset_hour), minute=int(sunset_minute),
                                    second=00, microsecond=0)

    if (sunset - datetime.now()).total_seconds() > 0:
        day_night = 'day'
    else:
        day_night = 'night'

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
    global icon, forecast_day_old, forecast_cond_old
    global forecast_high_old, forecast_low_old, icon_old, rss_once, feed_titles_old, feed_summary_old, tom_temp
    global tom_temp_old, day_night_old, out_temp_old, in_temp_old
    yield_me = ''
    if day_night != day_night_old:
        print(day_night)
        day_night_old = day_night
        yield_me += 'event: dayNight\n' + 'data: ' + day_night + '\n\n'
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
    if icon != icon_old:
        icon_old = icon
        yield_me += 'event: icon\n' + 'data: ' + icon + '\n\n'
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
        return render_template("index.html")

    @app.route('/poo')
    def try2():
        print('poo')
        return redirect(url_for('my_form'))

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80)

finally:
    sched.shutdown()