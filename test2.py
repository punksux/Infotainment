from urllib.request import Request, urlopen
import json
from datetime import datetime, timedelta
from operator import itemgetter

holidays = ["New Year\u2019s Day", "Groundhog Day", "Valentine\u2019s Day", "Washington\u2019s Birthday",
            "Saint Patrick\u2019s Day", "April Fools\u2019 Day", "Earth Day", "Star Wars Day", "Cinco de Mayo",
            "Mother\u2019s Day", "Memorial Day", "Flag Day", "Father\u2019s Day", "Independence Day", "Labor Day",
            "Halloween", "Veterans Day", "Thanksgiving Day", "Christmas", "New Year\u2019s Eve", "Easter"]
holiday_list = []


def get_holidays():
    global holiday_list
    holiday_website = 'http://holidayapi.com/v1/holidays?country=US&year=%s' % datetime.now().year
    w = open('tests/holiday.json')
    json_string = w.read()
    parsed_json = json.loads(json_string)
    for i in parsed_json['holidays']:
        for j in parsed_json['holidays'][i]:
            if j['name'] in holidays:
                holiday_list.append([j['date'], j['name']])

    holiday_list = sorted(holiday_list, key=itemgetter(0))

    return holiday_list

print(get_holidays())


def check_holiday():
    day = []
    for i in holiday_list:
        da = datetime.strptime(i[0], '%Y-%m-%d')
        if (da - datetime.now()).total_seconds() > 0:
            if (da - datetime.now()).days < 14:
                print()
            else:
                pass

            day = i
    else:
        day = 'Poo'

    return day

print(check_holiday())