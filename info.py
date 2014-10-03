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
import sports

weather_test = 200
on_pi = False
location = 84123
icon = ""
day = True
sun_or_moon_icon = ''
d_n_clouds = ''
rss_feeds = ['http://www.kutv.com/news/features/top-stories/stories/rss.xml',
             'http://www.utahutes.com/sports/m-footbl/headline-rss.xml',
             'http://feeds.bbci.co.uk/news/technology/rss.xml',
             'http://www.tmz.com/rss.xml']
rss_sources = ['KSL.com', 'UtahUtes.com', 'BBC Tech', 'TMZ.com']

weather_website = ('http://api.wunderground.com/api/c5e9d80d2269cb64/conditions/astronomy/forecast10day/alerts/' +
                   'hourly/q/%s.json' % location)
allergy_website = 'http://www.claritin.com/weatherpollenservice/weatherpollenservice.svc/getforecast/84123'

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


if on_pi:
    import urllib2
    #import RPi.GPIO as GPIO
    import socket
else:
    from urllib.request import Request, urlopen
    import urllib.error

app = Flask(__name__)

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

sched = Scheduler()
sched.start()

feed_no = 0


#    --==RSS Stuff==--
def get_rss():
    global feed, feed_titles, feed_summary, feed_titles_old, feed_summary_old, feed_no, rss_sources, feed_source
    feed_titles = []
    feed_summary = []
    feed = feedparser.parse(rss_feeds[feed_no])
    feed['items'] = feed['items'][:10]
    for i in feed['items']:
        feed_titles.append(i['title'])
        feed_summary.append(i['summary'])
    feed_source = rss_sources[feed_no]
    if feed_no == len(rss_feeds)-1:
        feed_no = 0
    else:
        feed_no += 1

#get_rss()
rss = sched.add_interval_job(get_rss, seconds=2*60)


def check_weather():
    global icon, forecast_day, forecast_cond, forecast_high, forecast_low, forecast_day_old, forecast_cond_old
    global forecast_high_old, forecast_low_old, tom_temp, sunset_hour, sunset_minute, day_night, city_name
    global observation_time, current_cond, predominant_pollen, allergy_forecast, full_weather, full_weather_old
    global sunrise_hour, sunrise_minute, relative_humidity, precip_today_string, wind_string, hourly_temps, alert
    if weather_test == 200:
        global something_wrong
        global f, g
        if on_pi:
            try:
                f = urllib2.urlopen(weather_website, timeout=3)
                g = urllib2.urlopen(allergy_website, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
                something_wrong = False
            except urllib2.URLError as e:
                logging.error('Data not retrieved because - %s' % e)
                something_wrong = True
            except socket.timeout:
                logging.error('Socket timed out')
                something_wrong = True
        else:
            try:
                #f = urlopen(weather_website, timeout=3)
                f = open('weather.json')
                req = Request(allergy_website, headers={'User-Agent': 'Mozilla/5.0'})
                #g = urlopen(req, timeout=3)
                g = open('allergy.json')

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

            json_string = f.read()
            #parsed_json = json.loads(json_string.decode("utf8"))
            parsed_json = json.loads(json_string)
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

            for i in range(0,12):
                hourly_temps.append(parsed_json['hourly_forecast'][i]['temp']['english'])
            print(hourly_temps)

            for i in range(0, 5):
                forecast_cond.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['icon'])
                forecast_day.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['date']['weekday'])
                forecast_high.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit'])
                forecast_low.append(parsed_json['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit'])

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
            #parsed_json = json.loads(json_string.decode('utf-8'))
            parsed_json = json.loads(json_string)
            set = parsed_json.find(':[')
            set2 = parsed_json.find('],')
            set3 = parsed_json.find('pp\":\"')
            set4 = parsed_json.find('\"time')
            predominant_pollen = parsed_json[set3+6: set4-2]
            allergy_forecast = parsed_json[set+2: set2]
            allergy_forecast = allergy_forecast.split(",")
            print(predominant_pollen)
            print(allergy_forecast)
            g.close()

            full_weather = [city_name, observation_time, current_cond, sunset_hour, sunset_minute, sunrise_hour,
                            sunrise_minute, relative_humidity, precip_today_string, wind_string]

    else:
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
        print(icon)
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
    global sun_or_moon_icon
    sunset = datetime.now().replace(hour=int(sunset_hour), minute=int(sunset_minute),
                                    second=00, microsecond=0)

    if (sunset - datetime.now()).total_seconds() > 0:
        day_night = 'day'
    else:
        day_night = 'night'

#check_weather()
weather = sched.add_interval_job(check_weather, seconds=60)


def get_temps_from_probes():
    global out_temp, in_temp
    if on_pi:
        pass
    else:
        out_temp = str(random.randrange(-32, 104))
        in_temp = str(random.randrange(32, 104))

get_temps_from_probes()
temps = sched.add_interval_job(get_temps_from_probes, seconds=10)

#     --==Sports Stuff==--
ncaa_team_names = {'ORS': 'Oregon State', 'ASU': 'Arizona State', 'ORE': 'Oregon', 'STA': 'Stanford', 'ARI': 'Arizona',
                   'COL': 'Colorado', 'UTH': 'Utah'}
nfl_team_names = {'SF': 'San Francisco', 'KC': 'Kansas City', 'DAL': 'Dallas', 'CHI': 'Chicago', 'ARI': 'Arizona',
                  'PHI': 'Philidelphia', 'STL': 'St. Louis', 'DEN': 'Denver', 'NO': 'New Orleans', 'NYG': 'New York',
                  'WAS': 'Washington', 'SEA': 'Seattle', 'OAK': 'Oakland', 'SD': 'San Diego'}


def football_weekly(week, team):
    global game, utah_week, sf_week, kc_week
    week_sched = sports.get_weekly_schedule(week, team)
    game = sched.add_date_job(start_football_scores, datetime.strptime(week_sched[3], '%Y-%m-%d %H:%M:%S'),
                              args=[week_sched[0], week_sched[1], week_sched[2]])

    week_sched[3] = datetime.strptime(week_sched[3], '%Y-%m-%d %H:%M:%S').strftime('%a %b %d %I:%M %p')
    if team == 'UTH':
        utah_week = week_sched
        for k, v in ncaa_team_names.items():
            utah_week[1] = utah_week[1].replace(k, v)
            utah_week[2] = utah_week[2].replace(k, v)
    elif team == 'SF':
        sf_week = week_sched
        for k, v in nfl_team_names.items():
            sf_week[1] = sf_week[1].replace(k, v)
            sf_week[2] = sf_week[2].replace(k, v)
    elif team == 'KC':
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
    global utah_score, sf_score, kc_score
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
#sched.print_jobs()

rss_once = False
day_once = False
icon_once = False
alert_once = False
utah_once = False
sf_once = False
kc_once = False

#     --==Streaming Stuff==--
def event_stream():
    global icon, forecast_day_old, forecast_cond_old, day_once, icon_once
    global forecast_high_old, forecast_low_old, icon_old, rss_once, feed_titles_old, feed_summary_old, tom_temp
    global tom_temp_old, day_night_old, out_temp_old, in_temp_old, feed_source_old, allergy_forecast_old
    global predominant_pollen_old,  full_weather_old, hourly_temps_old, alert_old, alert_once, utah_week_old
    global utah_once, utah_score_old, sf_week_old, kc_week_old, sf_once, kc_once, sf_score_old, kc_score_old
    yield_me = ''
    if day_night != day_night_old or day_once is False:
        day_night_old = day_night
        day_once = True
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
        yield_me += 'event: rssSum\n' + 'data: ' + json.dumps(feed_summary) + '\n\n'
    if feed_source != feed_source_old or rss_once is False:
        feed_source_old = feed_source
        rss_once = True
        yield_me += 'event: rssSource\n' + 'data: ' + feed_source + '\n\n'
    if icon != icon_old or icon_once is False:
        icon_old = icon
        icon_once = True
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
    if allergy_forecast != allergy_forecast_old:
        allergy_forecast_old = allergy_forecast
        yield_me += 'event: allergyForecast\n' + 'data: ' + json.dumps(allergy_forecast) + '\n\n'
    if predominant_pollen != predominant_pollen_old:
        predominant_pollen_old = predominant_pollen
        yield_me += 'event: predominantPollen\n' + 'data: ' + predominant_pollen + '\n\n'
    if full_weather != full_weather_old:
        full_weather_old = full_weather
        yield_me += 'event: fullWeather\n' + 'data: ' + json.dumps(full_weather) + '\n\n'
    if hourly_temps != hourly_temps_old:
        hourly_temps_old = hourly_temps
        yield_me += 'event: hourlyTemps\n' + 'data: ' + json.dumps(hourly_temps) + '\n\n'
    if alert != alert_old or alert_once is False:
        alert_old = alert
        alert_once = True
        yield_me += 'event: alert\n' + 'data: ' + json.dumps(alert) + '\n\n'
    if utah_week != utah_week_old or utah_once is False:
        utah_week_old = utah_week
        utah_once = True
        yield_me += 'event: utahInfo\n' + 'data: ' + json.dumps(utah_week) + '\n\n'
    if utah_score != utah_score_old:
        utah_score_old = utah_score
        yield_me += 'event: utahScore\n' + 'data: ' + json.dumps(utah_score) + '\n\n'
    if sf_week != sf_week_old or sf_once is False:
        sf_week_old = sf_week
        sf_once = True
        yield_me += 'event: sfInfo\n' + 'data: ' + json.dumps(sf_week) + '\n\n'
    if sf_score != sf_score_old:
        sf_score_old = sf_score
        yield_me += 'event: sfScore\n' + 'data: ' + json.dumps(sf_score) + '\n\n'
    if kc_week != kc_week_old or kc_once is False:
        kc_week_old = kc_week
        kc_once = True
        yield_me += 'event: kcInfo\n' + 'data: ' + json.dumps(kc_week) + '\n\n'
    if kc_score != kc_score_old:
        kc_score_old = kc_score
        yield_me += 'event: kcScore\n' + 'data: ' + json.dumps(kc_score) + '\n\n'

    yield yield_me

    time.sleep(0)


try:

    @app.route('/my_event_source')
    def sse_request():
        return Response(event_stream(), mimetype='text/event-stream')

    @app.route('/')
    def my_form():
        global rss_once, day_once, icon_once, alert_once, utah_once, sf_once, kc_once
        rss_once = False
        day_once = False
        icon_once = False
        alert_once = False
        utah_once = False
        sf_once = False
        kc_once = False
        return render_template("index.html")

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80)

finally:
    sched.shutdown()