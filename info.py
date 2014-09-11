from flask import Flask, request, render_template, url_for, redirect
import logging
import logging.handlers
from socket import timeout
import json
from datetime import datetime

weather_test = 100
on_pi = False
location = 84123
icon = ""
day = True
sun_or_moon_icon = ''
d_n_clouds = ''

templateData = {
    'icon': ['', '', ''],
    'clouds':  '',
    'sun_moon': '',
    'precip': '',
    'sunset_hour': '2',
    'sunset_minute': '00',
    'background': '',
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

            # print(parsed_json['current_observation']['weather'])
            # weather = parsed_json['current_observation']['weather'].lower()
            # precip_check = ['rain', 'snow', 'drizzle']
            # if any(x in weather for x in precip_check):
            #     precip = True
            # else:
            #     precip = False
            #
            # print(precip)
            sun_or_moon()
            set_icon()
            f.close()
    else:
        icon = "partlysunny"
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
    else:
        day = False
        sun_or_moon_icon = 'moon'
        d_n_clouds = 'night'
        templateData['background'] = '-moz-linear-gradient(top, #1f1f3f 0%, #141f31 100%);'


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

try:
    @app.route('/')
    def my_form():
        return render_template("index.html", **templateData)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80)

finally:
    pass