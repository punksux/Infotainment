from urllib.request import Request, urlopen
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
        rating_critics = i['ratings']['critics_score']
        rating_audience = i['ratings']['audience_score']
        synopsis = i['synopsis']
        poster = i['posters']['detailed']

        opening.append([title, rating, runtime, release_date, rating_rating, rating_critics, rating_audience,
                        synopsis, poster])

    return opening

#print(str(get_opening_movies()).replace('],', ']\n'))


def get_upcoming_movies():
    pass


def get_local_events():
    eventful_api = 'xJHGrFDwdj5qWgfW'
    eventful_website = 'http://api.eventful.com/rest/events/search?app_key=%s&location=Salt+Lake+City+UT&' \
                       'date=This+Week' % eventful_api


    f = ET.parse('eventful.xml')
    items = f.getroot()

    events = []

    for i in items[8]:

        title = i[0].text
        description = i[2].text
        start_time = i[3].text
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        if start_time.strftime('%I:%M') = '00:00':
            pass
        else:
            start_time = start_time.strftime('%B %d @ %I:%M %p')
        stop_time = i[4].text
        venue = i[12].text
        if i[36].find('url') is not None:
            image = i[36][0].text
        else:
            image = ''

        events.append([title, description, start_time, stop_time, venue, image])

    return events


#print(str(get_local_events()).replace('],', ']\n'))