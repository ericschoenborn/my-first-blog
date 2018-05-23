from datetime import datetime


def get_sprints(parts):

    all_sprints = []

    for part in parts['issues']:

        now = datetime.now().date()

        issue = part['key']
        part = part['fields']

        sprint_name = "NA"
        sprint_list = part['customfield_10000']
        sprint_dict = dict()
        days_remain = "NA"
        sprint_start_date = "NA"
        sprint_end_date = "NA"

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

            # Date and Time Remaining for the Sprint
            sprint_start = sprint_dict['startDate'].split("T")
            sprint_end = sprint_dict['endDate'].split("T")

            sprint_start_date = sprint_start[0]
            sprint_end_date = sprint_end[0]

            # add sprint only if active
            if state_sprint == "ACTIVE":

                if sprint_start[0] != '<null>' and sprint_end[0] != '<null>':
                    days_remain = (datetime.strptime(sprint_end[0], "%Y-%m-%d").date() - now).days
                add_sprint = True

                if len(all_sprints) > 0:
                    for items in all_sprints:

                        if name_sprint == items[0]:
                            add_sprint = False
                            break

                if add_sprint:
                    all_sprints.append([name_sprint, sprint_start_date, sprint_end_date, days_remain])

    return all_sprints
