from flask import Flask, render_template, Response, request, jsonify
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
import requests

album_info = []


def get_album(song2, artist2, album2, like2):
    global album_info
    last_fm_website = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&' \
                      'api_key=7e0ead667c3b37eb1ed9f3d16778fe38&artist=%s&album=%s&format=json' \
                      % (quote(artist2), quote(album2))
    chartlyrics_website = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?' \
                          'artist=%s&song=%s' % (quote(artist2), quote(song2))

    # q = urlopen(last_fm_website)
    # json_string = q.read()
    # parsed_json = json.loads(json_string.decode('utf-8'))
    # if 'image' in parsed_json['album']:
    #     album_art = parsed_json['album']['image'][3]['#text']
    # else:
    #     album_art = '/static/images/pandora/blank.jpg'
    # if 'wiki' in parsed_json['album']:
    #     album_sum = re.sub('<[^<]+?>', '', parsed_json['album']['wiki']['summary'])
    # else:
    #     album_sum = ''

    print('Getting lyrics')
    print(chartlyrics_website)
    t = ET.parse(urlopen(chartlyrics_website))
    items = t.getroot()
    lyrics = items[9].text
    print(items[9].text)


get_album('bugs', 'Pearl Jam', 'Sublime', '')