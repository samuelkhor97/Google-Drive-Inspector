'''
This is proposed to be the real main.py in the far future
It will do:
- start a local web server (bottle framework)
- load another file that handle web requests
-- that file will call functions from current main.py (propose to be renamed)
Requires: bottle
* read README.md for more instruction *
'''
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient import errors
import bottle
from bottle import route, run, template, static_file
import os

# add template directoryb
viewpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))
bottle.TEMPLATE_PATH.insert(0, viewpath)

# DEV:
from main import WIP_request_handler as request_list_all_users


@route("/static/<filepath>")
def css(filepath):
    return static_file(filepath, root=viewpath + "/static/")


@route('/')
def index():
    return template('index', content="Dynamically added content")


@route('/login')
def login():
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    return template('team_drives')


@route('/main')
def main():
    return request_list_all_users()


run(host='localhost', port=7878)
