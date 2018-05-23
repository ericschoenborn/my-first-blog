import json
import requests
from .get_time_log import get_time_log
from .config_connect import config, jira_url_request, request
from .get_sprints import get_sprints
from .get_issues import get_issues


def retrieve_jira_data(person):

    page = 0
    parts = retrieve_jira_data_by_page(person, page)
    issue_count = len(parts["issues"])
    total = parts["total"]

    while total != issue_count:
        page += 1
        tmp_parts = retrieve_jira_data_by_page(person, page)
        tmp_issues = tmp_parts["issues"]
        parts["issues"] = parts["issues"] + tmp_issues
        issue_count = len(parts["issues"])

    return parts


def retrieve_jira_data_by_page(person, page):
    start_index = 50 * page

    url = jira_url_request(config()) + "search?jql=assignee %3D " + person\
        + "%20%26%20status%20!%3D%20closed&startAt=" + str(start_index) + "&maxResults=50"

    auth = request(config())

    response = requests.get(url, auth=auth)
    parts = json.loads(response.text)

    return parts


def get_unverifiable_list():

    url = jira_url_request(config()) + "search?jql=filter=13800#"
    auth = request(config())
    response = requests.get(url, auth=auth)
    unverifiables = json.loads(response.text)
    unverifiable_list = []
    for items in unverifiables['issues']:
        unverifiable_list.append(items['key'])

    return unverifiable_list


def main(person):
    parts = retrieve_jira_data(person)
    main_array = []
    sprints = get_sprints(parts)
    # for i in sprints:
    #     print(Sprint.get_sprint(i))
    unverifiable = get_unverifiable_list()
    issues = get_issues(parts, unverifiable)
    # for i in issues:
    #     print(Issues.get_issue(i))

    time_log = get_time_log(person)
    # for i in time_log:
    #     print(TimeLog.get_time_log(i))

    main_array.append(sprints)
    main_array.append(issues)
    main_array.append(time_log)

    return main_array




if __name__ == "__main__":
    main()
