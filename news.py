from urllib.request import urlopen
import json
import time

#NY Times
newswire = '286730a4d43f4ec837576231d54a68a6:17:70264294'
event = '577077e3debf5850d22d644f9bc33388:0:70264294'

category = 'all'
categories = ['technology', 'u%2Es%2E', 'movies', 'sports', 'science', 'food']


def get_news():
    global category, i, image
    rss_feed = []
    for i in range(0, len(categories)):
        category = categories[i]
        website = 'http://api.nytimes.com/svc/news/v3/content/all/%s?' \
                  'api-key=286730a4d43f4ec837576231d54a68a6:17:70264294&limit=10' % category

        f = urlopen(website)
        json_string = f.read()
        parsed_json = json.loads(json_string.decode('utf-8'))
        f.close()

        for j in range(0, 10):
            title = parsed_json['results'][j]['title']
            summary = parsed_json['results'][j]['abstract']
            if parsed_json['results'][j]['multimedia'] != '':
                for k in range(0, len(parsed_json['results'][j]['multimedia'])):
                    if parsed_json['results'][j]['multimedia'][k]['format'] == 'Standard Thumbnail':
                        image = parsed_json['results'][j]['multimedia'][k]['url']
                    if parsed_json['results'][j]['multimedia'][k]['format'] == 'thumbLarge':
                        image = parsed_json['results'][j]['multimedia'][k]['url']
                        break
            else:
                image = ''
            link = parsed_json['results'][j]['url']
            category = 'U.S.' if category == 'u%2Es%2E' else category
            rss_feed.append([title, summary, image, link, category])

        time.sleep(2)

    return rss_feed
