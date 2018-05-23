import configparser
import requests
import os
from mysite.settings import CONFIG_PATH


def config():
    c = configparser.ConfigParser()
    c.read(['config.ini', os.path.expanduser(CONFIG_PATH)])

    return c


# jira requests
def request(config):
    usr = config['jira_auth']['usr']

    pas = config['jira_auth']['pass']

    r = (usr, pas)
    return r


def jira_url_request(config):
    url = config['jira']['endpoint']

    r = url
    return r


# confluence requests
def confluence_url_request(config):
    url = config['confluence']['endpoint']

    r = url
    return r


def con_request(config):
    usr = config['con_auth']['usr']

    pas = config['con_auth']['pass']

    r = (usr, pas)
    return r


# requests used for get_time_log
def token_config():
    c = configparser.ConfigParser()
    c.read('config.ini')

    return c


def token_request(config):
    headers = {
        'Authorization': config['idsrv']['auth_header']
    }

    payload = {
        'grant_type': 'client_credentials',
        'scope': 'jira-dataminer'
    }

    r = requests.post(config['idsrv']['url'], data=payload, headers=headers)

    return r
