from urllib.request import Request, urlopen
import json
import os
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET


#     --== Football ==--
def get_season_schedule(team):
    global website
    ncaa_season_website = 'http://api.sportsdatallc.org/ncaafb-t1/%s/REG/schedule.json?' \
                          'api_key=qnhb46ta6f9rzezkfjy7r4n5' % datetime.now().year

    nfl_season_website = 'http://api.sportsdatallc.org/nfl-t1/%s/REG/schedule.json?' \
                         'api_key=rn43y42wvev2xtzswtksk3r5' % datetime.now().year

    if team == 'UTH':
        website = 'season_sched.json'
    elif team == 'SF' or team == 'KC':
        website = 'nfl_season_sched.json'

    schedule = []
    f = open(website)
    json_string = f.read()
    parsed_json = json.loads(json_string.replace("O'", "O"))

    for i in range(0, len(parsed_json['weeks'])-1):
        for j in range(0, len(parsed_json['weeks'][i]['games'])):
            if parsed_json['weeks'][i]['games'][j]['away'] == team or \
               parsed_json['weeks'][i]['games'][j]['home'] == team:
                week = str(parsed_json['weeks'][i]['number'])
                home = parsed_json['weeks'][i]['games'][j]['home']
                away = parsed_json['weeks'][i]['games'][j]['away']
                time = datetime.strptime(parsed_json['weeks'][i]['games'][j]['scheduled'].split('+')[0],
                                         '%Y-%m-%dT%H:%M:%S')
                time -= timedelta(hours=6)
                time = time.strftime('%Y-%m-%d %H:%M:%S')
                status = parsed_json['weeks'][i]['games'][j]['status']
                venue = parsed_json['weeks'][i]['games'][j]['venue']['name']
                if 'broadcast' in parsed_json['weeks'][i]['games'][j]:
                    tv = parsed_json['weeks'][i]['games'][j]['broadcast']['network']
                else:
                    tv = ''
                schedule.append([week, home, away, time, status, venue, tv])
                break
        else:
            time = datetime.strptime(parsed_json['weeks'][i]['games'][0]['scheduled'].split('+')[0],
                                     '%Y-%m-%dT%H:%M:%S')
            time -= timedelta(hours=6)
            time = time.strftime('%Y-%m-%d %H:%M:%S')
            schedule.append([str(parsed_json['weeks'][i]['number']), team, 'BYE', time, '', '', ''])
    f.close()
    return schedule


def get_weekly_schedule(week, team):
    global website
    ncaa_weekly_website = 'http://api.sportsdatallc.org/ncaafb-t1/%s/REG/%s/schedule.json?' \
                          'api_key=qnhb46ta6f9rzezkfjy7r4n5' % (datetime.now().year, week)

    nfl_season_website = 'http://api.sportsdatallc.org/nfl-t1/%s/REG/%s/schedule.json?' \
                         'api_key=rn43y42wvev2xtzswtksk3r5' % (datetime.now().year, week)

    if team == 'UTH':
        website = 'week_sched.json'
    elif team == 'SF' or team == 'KC':
        website = 'nfl_week_sched.json'

    week = []
    f = open(website)
    json_string = f.read()
    parsed_json = json.loads(json_string.replace("O'", "O"))

    for j in range(0, len(parsed_json['games'])):
            if parsed_json['games'][j]['away'] == team or \
               parsed_json['games'][j]['home'] == team:
                week = parsed_json['number']
                home = parsed_json['games'][j]['home']
                away = parsed_json['games'][j]['away']
                time = datetime.strptime(parsed_json['games'][j]['scheduled'].split('+')[0],
                                         '%Y-%m-%dT%H:%M:%S')
                time -= timedelta(hours=6)
                time = time.strftime('%Y-%m-%d %H:%M:%S')
                status = parsed_json['games'][j]['status']
                venue = parsed_json['games'][j]['venue']['name']
                if 'broadcast' in parsed_json['games'][j]:
                    tv = parsed_json['games'][j]['broadcast']['network']
                else:
                    tv = ''
                week = [week, home, away, time, status, venue, tv]
    f.close()
    return week


def get_boxscore(week, home, away):
    global website
    ncaa_boxscore_website = 'http://api.sportsdatallc.org/ncaafb-t1/%s/REG/%s/%s/%s/boxscore.json?' \
                            'api_key=qnhb46ta6f9rzezkfjy7r4n5' % (str(datetime.now().year), week, away, home)

    nfl_boxscore_website = 'http://api.sportsdatallc.org/nfl-t1/%s/REG/%s/%s/%s/boxscore.json?' \
                           'api_key=rn43y42wvev2xtzswtksk3r5' % (str(datetime.now().year), week, away, home)

    if home == 'UTH' or away == 'UTH':
        website = 'boxscore.json'
    else:
        website = 'nfl_boxscore.json'

    f = open(website)
    json_string = f.read()
    parsed_json = json.loads(json_string.replace("O'", "O"))

    status = parsed_json['status']
    quarter = parsed_json['quarter']
    clock = parsed_json['clock']
    home_points = parsed_json['home_team']['points']
    away_points = parsed_json['away_team']['points']

    scores = [status, quarter, clock, home_points, away_points]

    return scores

#print(str(get_season_schedule('SF')).replace("],", "]\n"))


#     --== Soccer ==--
def get_soccer_season():
    global website
    ncaa_season_website = 'http://api.sportsdatallc.org/soccer-t2/na/matches/schedule.xml?' \
                          'api_key=q57zpdq4d7mvmtns4uxk92f8 '

    schedule = []
    f = ET.parse('mls_season_sched.xml')
    items = f.getroot()

    for i in items[0]:
        if i[3].attrib['alias'] == 'SAL' or i[4].attrib['alias'] == 'SAL':
            match_id = i.attrib['id']
            home = i[3].attrib['name']
            away = i[4].attrib['name']
            time = datetime.strptime(i.attrib['scheduled'], '%Y-%m-%dT%H:%M:%SZ')
            time -= timedelta(hours=6)
            time = time.strftime('%Y-%m-%d %H:%M:%S')
            status = i.attrib['status']
            if 'name' in i[5].attrib:
                venue = i[5].attrib['name']
            else:
                venue = ''
            schedule.append([match_id, home, away, time, status, venue])

    return schedule


def soccer_scores(game_id):
    global website
    ncaa_season_website = 'http://api.sportsdatallc.org/soccer-t2/na/matches/schedule.xml?' \
                          'api_key=q57zpdq4d7mvmtns4uxk92f8 '

    schedule = []
    f = ET.parse('mls_season_sched.xml')
    items = f.getroot()

    for i in items[0]:
        if i[3].attrib['alias'] == 'SAL' or i[4].attrib['alias'] == 'SAL':
            match_id = i.attrib['id']
            home = i[3].attrib['name']
            away = i[4].attrib['name']
            time = datetime.strptime(i.attrib['scheduled'], '%Y-%m-%dT%H:%M:%SZ')
            time -= timedelta(hours=6)
            time = time.strftime('%Y-%m-%d %H:%M:%S')
            status = i.attrib['status']
            if 'name' in i[5].attrib:
                venue = i[5].attrib['name']
            else:
                venue = ''
            schedule.append([match_id, home, away, time, status, venue])

    return schedule
#print(str(get_soccer_season()).replace('],', ']\n'))