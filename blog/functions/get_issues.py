import operator
from datetime import datetime
from .confluence_data import dpl_title_list
from .defcon import calculate_defcon


def get_issues(parts, unverifiable_list):

    dpl_plan_list = dpl_title_list()
    issue_list = []
    all_sprints = []

    for part in parts['issues']:

        issue = part['key']
        part = part['fields']
        unverifiable = "N"

        if issue in unverifiable_list:
            unverifiable = "Y"

        # current date
        now = datetime.now().date()

        # get age from date created
        date = part['created'].split("T")
        age = abs((datetime.strptime(date[0], "%Y-%m-%d").date() - now).days)

        # get idle from customfield
        date = part['customfield_13807']
        idle = abs((datetime.strptime(date, "%Y-%m-%d").date() - now).days)

        # time remaining from timespent and aggregate time estimate
        if part['aggregatetimeestimate'] is None:
            remain = "NA"
        else:
            if part['timespent'] is None:
                remain = part['aggregatetimeestimate']
            else:
                remain = (int(part['aggregatetimeestimate']) - int(part['timespent']) / 60) / 60

        # time spent from time spent
        if part['timespent'] is None:
            time_spent = 0
        else:
            time_spent = (int(part['timespent']) / 60) / 60

        # -------------------------------------------------------------------------

        sprint_name = "NA"
        sprint_list = part['customfield_10000']
        sprint_dict = dict()

        if sprint_list is not None:

            # creating dictionary of sprint data
            for sprint in sprint_list:

                sprint_string = sprint
                sprint_ls = sprint.split(",")

                for item in sprint_ls:
                    item = item.split("=")  # in order to access the name of the sprint

                    if len(item) > 1:
                        sprint_dict[item[0]] = item[1]

            state_sprint = sprint_dict['state']
            name_sprint = sprint_dict['name']

            # only add sprint if active
            if state_sprint == "ACTIVE":
                sprint_name = name_sprint
        # ------------------------------------------------------------------------------------------------------

        ####################################---VARIABLES----##########################################
        summary = part['summary']
        priority = part['priority']['id']
        due = part['duedate']
        status = part['status']['name']
        deployable = "N"
        deployable_link = "NA"
        ##############################################################################################

        for list in dpl_plan_list:
            for item in list:
                if item == issue:
                    deployable = list[0]
                    deployable_link = list[1]

        if due is None:
            due = "NA"

        defcon = calculate_defcon(idle, status, remain, deployable, issue, due, now, unverifiable)

        issue_list.append([issue, summary, priority, due, status, idle, deployable, unverifiable, sprint_name, time_spent, age, remain,
                                 defcon])
        issue_list = sorted(issue_list, key=operator.itemgetter(4, 2, 3))
    return issue_list
