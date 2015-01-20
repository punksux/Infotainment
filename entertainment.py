from urllib.request import urlopen
import json
from xml.etree import ElementTree as ET
import datetime
import requests
import bs4
from urllib.parse import quote
import random


def get_opening_movies():
    rotten_tomatoes_website = 'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/opening.json?' \
                              'apikey=j66zchayd6megzhvzhp33dm9&limit=10'

    f = urlopen(rotten_tomatoes_website)
    json_string = f.read()
    parsed_json = json.loads(json_string.decode('utf-8'))
    f.close()

    opening = []
    for i in parsed_json['movies']:
        title = i['title']
        trailer = search_trailer(title)
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
        actors = []
        for j in i['abridged_cast']:
            actors.append(j['name'])
        actors = actors[:3]
        link = i['links']['alternate']

        opening.append([title, rating, runtime, release_date, rating_rating, rating_critics, rating_audience,
                        synopsis, poster, actors, link, trailer])

    return opening


# print(str(get_opening_movies()).replace('],', ']\n'))


def search_trailer(title):
    youtube_search = 'https://www.googleapis.com/youtube/v3/search?part=snippet&order=relevance&q=%s&' \
                     'safeSearch=moderate&key=AIzaSyCEXmTD14AKz0RLWCOw7aIRhW-bIZtqk8o' % quote(title + ' official trailer')

    f = urlopen(youtube_search)
    json_string = f.read()
    parsed_json = json.loads(json_string.decode('utf-8'))
    f.close()
    trailer_id = parsed_json['items'][0]['id']['videoId']
    trailer_link = "//www.youtube.com/embed/%s?rel=0&showinfo=0&iv_load_policy=3" % trailer_id
    return trailer_link


def get_local_events():
    eventful_website = 'http://api.eventful.com/rest/events/search?app_key=xJHGrFDwdj5qWgfW&' \
                       'location=Salt+Lake+City+UT&date=This+Week&mature=normal&' \
                       'category=music%2Ccomedy%2Cart%2Ctechnology%2Cfamily_fun_kids'

    f = ET.parse(urlopen(eventful_website))
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
        url = i[1].text

        events.append([title, description, start_time, stop_time, venue, image, url])

    return events


j_ids = []


def jeopardy():
    jservice_website = 'http://jservice.io/api/random?count=1'

    f = urlopen(jservice_website)
    json_string = f.read()
    parsed_json = json.loads(json_string.decode('utf-8'))
    f.close()

    id_no = parsed_json[0]['id']

    if id_no in j_ids:
        jeopardy()
    else:
        answer = parsed_json[0]['answer']
        question = parsed_json[0]['question']
        value = parsed_json[0]['value']
        category = parsed_json[0]['category']['title']

        if len(j_ids) > 99:
            j_ids.pop(0)

        j_ids.append(id_no)

        print([answer, question, value, category])
        return [answer, question, value, category]

old_cheez = ''


def cheezburger():
    global old_cheez
    r = requests.get('http://www.cheezburger.com/')
    soup = bs4.BeautifulSoup(r.text)
    image = soup.find(class_='event-item-lol-image')
    source = image['src']
    if old_cheez != source:
        old_cheez = source
        print(source)
        return source
    else:
        return ''

old_flickr = []


def flickr():
    global old_flickr, image_url, title, location, description
    places = ['salt lake city', 'santa cruz', 'san francisco', 'utah', 'united states', 'california']

    place = random.choice(places)
    website = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&' \
              'api_key=52e4dddd8831873f04816ae4b0b3224b&text=%s+landscape&safe_search=1&' \
              'content_type=1&format=json&nojsoncallback=1' % quote(place)

    f = urlopen(website)
    json_string = f.read()
    parsed_json = json.loads(json_string.decode('utf-8'))
    f.close()

    for i in range(0, len(parsed_json['photos']['photo'])):
        if parsed_json['photos']['photo'][i]['id'] in old_flickr:
            continue
        else:
            farm_id = parsed_json['photos']['photo'][i]['farm']
            server_id = parsed_json['photos']['photo'][i]['server']
            id_no = parsed_json['photos']['photo'][i]['id']
            secret = parsed_json['photos']['photo'][i]['secret']
            image_url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % (farm_id, server_id, id_no, secret)

            website2 = 'https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=52e4dddd8831873f04816ae4b0b3224b&photo_id=%s&format=json&nojsoncallback=1' % id_no
            g = urlopen(website2)
            json_string2 = g.read()
            parsed_json2 = json.loads(json_string2.decode('utf-8'))
            g.close()

            title = parsed_json2['photo']['title']['_content']
            location = parsed_json2['photo']['owner']['location']
            description = parsed_json2['photo']['description']['_content']

            old_flickr.append(id_no)
            if len(old_flickr) > 20:
                old_flickr.pop(0)
            break

    return [title, description, location, image_url]


old_true = []
old_lol = []


def sotruefacts():
    global old_true, old_lol, got_one
    got_one = False
    websites = ['http://www.sotruefacts.com/', 'http://www.lolsotrue.com/']
    website = random.choice(websites)

    r = requests.get(website)
    soup = bs4.BeautifulSoup(r.text)
    if website == websites[0]:
        image = soup.find(class_='small')
        source = image.img['src']
        start = source.find('rules/')
        end = source.find('.png')
        number = source[start + 6:end]
        while got_one is False:
            rand = random.randint(1, int(number))
            if rand not in old_true:
                old_true.append(rand)
                if len(old_true) > 40:
                    old_true.pop(0)
                src = 'http://www.sotruefacts.com/rules/%s.png' % rand
                print(src)
                got_one = True
                return src
    else:
        image = soup.find(class_='image')
        source = image.a.img['src']
        start = source.find('rules/')
        end = source.find('.png')
        number = source[start + 6:end]
        while got_one is False:
            rand = random.randint(1, int(number))
            if rand not in old_lol:
                old_lol.append(rand)
                if len(old_lol) > 40:
                    old_lol.pop(0)
                src = 'http://www.lolsotrue.com/rules/%s.png' % rand
                print(src)
                got_one = True
                return src

# sotruefacts()