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
from drive_functions import *
import bottle
from bottle import route, run, template, static_file, redirect
import os

# add template directoryb
viewpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))
bottle.TEMPLATE_PATH.insert(0, viewpath)
service = None


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
        flow = client.flow_from_clientsecrets(
            'credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    global service
    service = build('drive', 'v3', http=creds.authorize(Http()))

    return redirect('/team_drives')


@route('/team_drives')
def list_team_drives():
    drive_ids = getDriveIds(service)
    for drive_name in drive_ids:
        drive_ids[drive_name] = '/team_drives/' + drive_ids[drive_name]

    return template('team_drives', drive_ids=drive_ids)


@route('/team_drives/<team_drive_id>')
def team_contributions(team_drive_id):
    print("yes")


@route('/main')
def main():
    return request_list_all_users()


run(host='localhost', port=7878)
