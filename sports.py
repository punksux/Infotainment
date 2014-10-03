from urllib.request import Request, urlopen
import json
import os
from datetime import datetime, timedelta


def get_utah_season_schedule():
    ncaa_season_website = 'http://api.sportsdatallc.org/ncaafb-t1/%s/REG/schedule.json?' \
                          'api_key=qnhb46ta6f9rzezkfjy7r4n5' % datetime.now().year
    if not os.path.isfile('season_sched.json') or os.path.getsize('season_sched.json') <= 0:
        h = urlopen(ncaa_season_website)
        ncaa_sched = h.read()
        ncaa_sched = json.loads(ncaa_sched.replace("O'", "O").decode('utf-8'))
        with open('season_sched.json', 'w') as outfile:
            json.dump(ncaa_sched, outfile)
        print('New info')

    utah_schedule = []
    f = open('season_sched.json')
    json_string = f.read()
    parsed_json = json.loads(json_string.replace("O'", "O"))

    for i in range(0, len(parsed_json['weeks'])-1):
        for j in range(0, len(parsed_json['weeks'][i]['games'])):
            if parsed_json['weeks'][i]['games'][j]['away'] == 'UTH' or \
               parsed_json['weeks'][i]['games'][j]['home'] == 'UTH':
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
                utah_schedule.append([week, home, away, time, status, venue, tv])
                break
        else:
            time = datetime.strptime(parsed_json['weeks'][i]['games'][0]['scheduled'].split('+')[0],
                                     '%Y-%m-%dT%H:%M:%S')
            time -= timedelta(hours=6)
            time = time.strftime('%Y-%m-%d %H:%M:%S')
            utah_schedule.append([str(parsed_json['weeks'][i]['number']), 'bye', 'bye', time, '', '', ''])
    f.close()
    return utah_schedule


def get_utah_weekly_schedule(week):
    ncaa_weekly_website = 'http://api.sportsdatallc.org/ncaafb-t1/%s/REG/%s/schedule.json?' \
                          'api_key=qnhb46ta6f9rzezkfjy7r4n5' % (datetime.now().year, week)

    utah_week = []
    f = open('week_sched.json')
    json_string = f.read()
    parsed_json = json.loads(json_string.replace("O'", "O"))

    for j in range(0, len(parsed_json['games'])):
            if parsed_json['games'][j]['away'] == 'UTH' or \
               parsed_json['games'][j]['home'] == 'UTH':
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
                utah_week = [week, home, away, time, status, venue, tv]
    f.close()
    return utah_week


def get_boxscore(week, home, away):
    ncaa_boxscore_website = 'http://api.sportsdatallc.org/ncaafb-t1/%s/REG/%s/%s/%s/boxscore.json?' \
                            'api_key=qnhb46ta6f9rzezkfjy7r4n5' % (str(datetime.now().year), week, away, home)
    f = open('boxscore.json')
    json_string = f.read()
    parsed_json = json.loads(json_string.replace("O'", "O"))

    status = parsed_json['status']
    quarter = parsed_json['quarter']
    clock = parsed_json['clock']
    home_points = parsed_json['home_team']['points']
    away_points = parsed_json['away_team']['points']

    scores = [status, quarter, clock, home_points, away_points]

    return scores

#print(str(get_utah_season_schedule()).replace("],", "]\n"))

