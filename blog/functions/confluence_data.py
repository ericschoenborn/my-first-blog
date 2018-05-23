import json
import requests
from .config_connect import config, confluence_url_request, con_request

# separate calls for data as one function
def dpl_title_list():
    url_root = confluence_url_request(config())
    url = url_root + "/rest/api/content/search?cql=(type=page and space=DEP and title ~ '2018' and (title ~ WIP or title ~ Ready))"
    auth = con_request(config())

    url2_Part3 = "/child?expand=page.body.view"

    response = requests.get(url, auth=auth)
    deploy_file = json.loads(response.text)

    info = deploy_file['results']

    dpl_plan_list = []

    for data in info:

        team_url_data = data['_expandable']['history']
        team_url_string = team_url_data.replace('/history', '')

        new_url = url_root + team_url_string + url2_Part3
        response = requests.get(new_url, auth=auth)
        deploy_file = json.loads(response.text)
        info2 = deploy_file['page']['results']

        for new_data in info2:

            startLine = new_data['body']['view']['value'].find("jqlQuery=key in (")
            endline = new_data['body']['view']['value'].find(")", startLine + 1) + 1

            startLine2 = new_data['body']['view']['value'].find("jqlQuery=key =")
            endline2 = new_data['body']['view']['value'].find("|", startLine2 + 1) - 1

            sub_list = []
            sub_list.append(new_data['title'])
            sub_list.append("NA")

            if startLine != -1:
                tmp = url_root + new_data['_links']['tinyui']
                sub_list[1] = tmp

                startLine = startLine + 17
                tmp = new_data['body']['view']['value'][startLine:endline]
                tmp = tmp.split(",")

                for i in tmp:
                    i = i.strip()
                    i = i.strip("&#x9;")
                    i = i.strip(")")
                    sub_list.append(i)
                    dpl_plan_list.append(sub_list)
            elif startLine2 != -1:
                startLine2 = startLine2 + 15
                tmp = url_root + new_data['_links']['tinyui']
                sub_list[1] = tmp

                tmp = new_data['body']['view']['value'][startLine2:endline2]
                sub_list.append(tmp)
                dpl_plan_list.append(sub_list)

    return dpl_plan_list
