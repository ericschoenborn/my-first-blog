import json
import requests
from datetime import date, timedelta
from .config_connect import token_config, token_request


def get_time_log(user_name):
    time_log2=[]
    today = date.today()
    prev_day = today - timedelta(days=1)

    if date.weekday(prev_day) == 5:  # if it's Saturday
        prev_day = prev_day - timedelta(days=1)

    elif date.weekday(prev_day) == 6:  # if it's Sunday
        prev_day = prev_day - timedelta(days=2)

    response = token_request(token_config())
    tmp = json.loads(response.text)

    url = "https://prv.prd.mvpbanking.com/jira-dataminer/api/v1/work-logs?username=" + user_name + "&date=" + prev_day.strftime(
        '%y%m%d')

    response2 = requests.get(url, headers={"Authorization": "Bearer " + tmp['access_token']})
    time_sheet = json.loads(response2.text)
    overall_time = 0
    time_log = []

    for times in time_sheet:
        overall_time += times['timeHours']
        time_log.append([times['issue'], times['description'], times['timeHours']])

    return time_log
