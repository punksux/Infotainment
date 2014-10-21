from urllib.request import Request, urlopen
import urllib

rotten_tomatoes_type = 'opening'
import json
from xml.etree import ElementTree as ET
import datetime

rotten_tomatoes_api = 'j66zchayd6megzhvzhp33dm9'
rotten_tomatoes_website = 'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/%s.json?apikey=%s&limit=10' \
                          % (rotten_tomatoes_type, rotten_tomatoes_api)


def get_opening_movies():
    f = open('rt_opening.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)

    opening = []
    for i in parsed_json['movies']:
        title = i['title']
        rating = i['mpaa_rating']
        runtime = i['runtime']
        release_date = i['release_dates']['theater']
        if 'critics_rating' in i['ratings']:
            rating_rating = i['ratings']['critics_rating']
        else:
            rating_rating = ''
        if i['ratings']['critics_score'] == -1:
            rating_critics = '-'
        else:
            rating_critics = i['ratings']['critics_score']
        rating_audience = i['ratings']['audience_score']
        synopsis = i['synopsis']
        synopsis = synopsis[:synopsis.find('(C)')][:synopsis.find('(c)')]
        poster = i['posters']['detailed']

        opening.append([title, rating, runtime, release_date, rating_rating, rating_critics, rating_audience,
                        synopsis, poster])

    return opening


# print(str(get_opening_movies()).replace('],', ']\n'))


def get_upcoming_movies():
    pass


def get_local_events():
    eventful_api = 'xJHGrFDwdj5qWgfW'
    eventful_website = 'http://api.eventful.com/rest/events/search?app_key=xJHGrFDwdj5qWgfW&' \
                       'location=Salt+Lake+City+UT&date=This+Week&mature=normal&' \
                       'category=music%2Ccomedy%2Cart%2Ctechnology%2Cfamily_fun_kids'

    f = ET.parse('eventful.xml')
    items = f.getroot()

    events = []

    for i in items[8]:

        title = i[0].text
        description = i[2].text
        start_time = i[3].text
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        if start_time.strftime('%H:%M') == '00:00':
            start_time = start_time.strftime('%B %d')
        else:
            start_time = start_time.strftime('%B %d <br /> %I:%M %p')
        stop_time = i[4].text
        if stop_time is not None:
            stop_time = datetime.datetime.strptime(stop_time, '%Y-%m-%d %H:%M:%S')
            if stop_time.strftime('%H:%M') == '00:00':
                stop_time = stop_time.strftime('%B %d')
            else:
                stop_time = stop_time.strftime('%B %d %I:%M %p')
        venue = i[12].text
        if i[36].find('url') is not None:
            image = i[36][0].text
        else:
            image = ''

        events.append([title, description, start_time, stop_time, venue, image])

    return events


    #print(str(get_local_events()).replace('],', ']\n'))