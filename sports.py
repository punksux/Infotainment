from urllib.request import Request, urlopen
import json
import os
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

ncaa_api_key = 'qnhb46ta6f9rzezkfjy7r4n5'
nfl_api_key = 'rn43y42wvev2xtzswtksk3r5'


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
                week = parsed_json['weeks'][i]['number']
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
            schedule.append([parsed_json['weeks'][i]['number'], team, 'BYE', time, '', '', ''])
    f.close()
    return schedule


def get_weekly_schedule(week, team):
    global website, week_sched
    ncaa_weekly_website = 'http://api.sportsdatallc.org/ncaafb-t1/%s/REG/%s/schedule.json?' \
                          'api_key=qnhb46ta6f9rzezkfjy7r4n5' % (datetime.now().year, week)

    nfl_season_website = 'http://api.sportsdatallc.org/nfl-t1/%s/REG/%s/schedule.json?' \
                         'api_key=rn43y42wvev2xtzswtksk3r5' % (datetime.now().year, week)

    if team == 'UTH':
        website = 'week_sched.json'
        #website = ncaa_weekly_website
    elif team == 'SF' or team == 'KC':
        website = 'nfl_week_sched.json'
        #website = nfl_season_website

    week_sched = []
    f = open(website)
    json_string = f.read()
    parsed_json = json.loads(json_string.replace("O'", "O"))
    #parsed_json = json.loads(json_string.decode('utf-8'))
    for j in range(0, len(parsed_json['games'])):
        if parsed_json['games'][j]['away'] == team or parsed_json['games'][j]['home'] == team:
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
            week_sched = [week, home, away, time, status, venue, tv]
            break
    else:
        week_sched = [int(week), team, 'BYE', '', '', '', '']

    f.close()
    return week_sched


def get_boxscore(week, home, away):
    global website
    ncaa_boxscore_website = 'http://api.sportsdatallc.org/ncaafb-t1/%s/REG/%s/%s/%s/boxscore.json?' \
                            'api_key=qnhb46ta6f9rzezkfjy7r4n5' % (str(datetime.now().year), week, away, home)

    nfl_boxscore_website = 'http://api.sportsdatallc.org/nfl-t1/%s/REG/%s/%s/%s/boxscore.json?' \
                           'api_key=rn43y42wvev2xtzswtksk3r5' % (str(datetime.now().year), week, away, home)

    if home == 'UTH' or away == 'UTH':
        website = 'boxscore.json'
        #website = ncaa_boxscore_website
    else:
        website = 'nfl_boxscore.json'

    f = open(website)
    json_string = f.read()
    parsed_json = json.loads(json_string)

    status = parsed_json['status']
    if 'quarter' in parsed_json:
        quarter = parsed_json['quarter']
    else:
        quarter = ''
    if 'clock' in parsed_json:
        clock = parsed_json['clock']
    else:
        clock = ''
    home_points = parsed_json['home_team']['points']
    away_points = parsed_json['away_team']['points']

    scores = [status, quarter, clock, home_points, away_points]

    return scores


def get_key(item):
    return item[4]


def get_ncaa_standings(week):
    global standings_website, rankings_website
    ncaa_standings_website = 'http://api.sportsdatallc.org/ncaafb-t1/teams/FBS/%s/REG/standings.json?' \
                             'api_key=qnhb46ta6f9rzezkfjy7r4n5' % datetime.now().year

    standings_website = 'ncaa_standings.json'

    f = open(standings_website)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    p12 = []
    for j in range(0, len(parsed_json['division']['conferences'])):
        if parsed_json['division']['conferences'][j]['name'] == 'Pac-12':
            for s in range(0, len(parsed_json['division']['conferences'][j]['teams'])):
                name = parsed_json['division']['conferences'][j]['teams'][s]['market']
                subdiv = parsed_json['division']['conferences'][j]['teams'][s]['subdivision']
                total_wins = parsed_json['division']['conferences'][j]['teams'][s]['overall']['wins']
                total_losses = parsed_json['division']['conferences'][j]['teams'][s]['overall']['losses']
                conf_wins = parsed_json['division']['conferences'][j]['teams'][s]['in_conference']['wins']
                conf_losses = parsed_json['division']['conferences'][j]['teams'][s]['in_conference']['losses']
                p12.append([name, subdiv, total_wins, total_losses, conf_wins, conf_losses])

    p12n = []
    p12s = []
    for i in p12:
        if i[1] == 'PAC-12-NORTH':
            p12n.append(i)
        else:
            p12s.append(i)

    p12n.sort(key=get_key, reverse=True)
    p12s.sort(key=get_key, reverse=True)

    p12 = p12n + p12s
    return p12

#print(str(get_standings('7', 'UTH')).replace("],", "]\n"))
#print(str(get_season_schedule('SF')).replace("],", "]\n"))


def get_ncaa_rankings(week):
    global rankings_website
    ncaa_rankings_website = 'http://api.sportsdatallc.org/ncaafb-t1/polls/AP25/%s/%s/rankings.json?' \
                            'api_key=qnhb46ta6f9rzezkfjy7r4n5' % (datetime.now().year, week)

    rankings_website = 'ncaa_rankings.json'

    f = open(rankings_website)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    rankings = []
    for i in range(0, len(parsed_json['rankings'])):
        r = parsed_json['rankings'][i]
        rankings.append([r['market'], r['wins'], r['losses']])

    return rankings

#print(str(get_rankings(7, 'UTH')).replace('],', ']\n'))


def get_nfl_rankings():
    nfl_rankings_website = 'http://api.sportsdatallc.org/nfl-t1/teams/%s/rankings.json?api_key=%s' \
                           % (datetime.now().year, nfl_api_key)

    nfl_standings_website = 'http://api.sportsdatallc.org/nfl-t1/teams/%s/REG/standings.json?api_key=%s' \
                            % (datetime.now().year, nfl_api_key)

    f = open('nfl_rankings.json')
    json_string = f.read()
    rankings_json = json.loads(json_string)
    rankings = []

    f = open('nfl_standings.json')
    json_string = f.read()
    standings_json = json.loads(json_string)

    for i in rankings_json['conferences']:
        for j in i['divisions']:
            for k in j['teams']:
                rankings.append([j['name'], k['market'], k['name']])

    for h in rankings:
        for i in standings_json['conferences']:
            for j in i['divisions']:
                for k in j['teams']:
                    if h[1] == k['market']:
                        h.extend([k['overall']['wins'], k['overall']['losses'],
                                  k['in_conference']['wins'], k['in_conference']['losses']])

    return rankings
#print(str(get_nfl_rankings()).replace('],', ']\n'))


#     --== Soccer ==--
def get_soccer_season():
    global website
    mls_season_website = 'http://api.sportsdatallc.org/soccer-t2/na/matches/schedule.xml?' \
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
    mls_boxscore_website = 'http://api.sportsdatallc.org/soccer-t2/na/matches/%s/boxscore.xml?' \
                           'api_key=q57zpdq4d7mvmtns4uxk92f8' % game_id

    schedule = []
    f = ET.parse('mls_boxscore.xml')
    items = f.getroot()

    if 'score' in items[0][0][5].attrib:
        home_points = items[0][0][5].attrib['score']
    else:
        home_points = '0'
    if 'score' in items[0][0][6].attrib:
        away_points = items[0][0][6].attrib['score']
    else:
        away_points = '0'
    status = items[0][0].attrib['status']
    period = items[0][0].attrib['period']

    scores = [status, period, home_points, away_points]

    return scores


def get_soccer_standings():
    mls_standings_website = 'http://api.sportsdatallc.org/soccer-t2/na/teams/standing.xml?' \
                            'api_key=q57zpdq4d7mvmtns4uxk92f8'

    standings = []
    f = ET.parse('mls_standings.xml')
    items = f.getroot()

    for i in items[0]:
        if i.attrib['country'] == 'United States':
            for j in i[0][0]:
                standings.append([j.attrib['name'], j.attrib['win'], j.attrib['draw'],
                                  j.attrib['loss']])

    return standings

#print(str(get_soccer_standings()).replace('],', ']\n'))