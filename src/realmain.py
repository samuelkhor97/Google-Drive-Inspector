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
from d_parser import D_Parser
from threading import Thread
import bottle
from bottle import route, run, template, static_file, redirect, request
import os

# add template directoryb
viewpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))
bottle.TEMPLATE_PATH.insert(0, viewpath)
service = None
flow = None


@route("/static/<filepath>")
def css(filepath):
    return static_file(filepath, root=viewpath + "/static/")


@route('/')
def index():
    return template('index')


@route('/login')
def login():
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        global flow
        flow = client.flow_from_clientsecrets(
            'credentials.json', scope=SCOPES, redirect_uri='http://localhost:7878/login/return')
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        global service
        service = build('drive', 'v3', http=creds.authorize(Http()))
        return redirect('/team_drives')


@route('/login/return')
def login_return():
    global flow
    code = request.query.code
    creds = flow.step2_exchange(code)
    del flow
    file.Storage('token.json').put(creds)
    global service
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return redirect('/team_drives')


@route('/team_drives')
def list_team_drives():
    drive_ids = getDriveIds(service)
    for drive_name in drive_ids:
        drive_ids[drive_name] = '/loading/' + drive_ids[drive_name]

    return template('team_drives', drive_ids=drive_ids)


def load_file_revisions(team_drive_id, service):
    file_revisions = get_file_revisions(team_drive_id, service)
    return template('team_contributions', file_revisions=file_revisions)


@route('/loading/<team_drive_id>')
def loading(team_drive_id):
    thr = Thread(target=load_file_revisions, args=[team_drive_id, service])
    thr.start()
    return template('loading')


@route('/team_drives/<team_drive_id>')
def team_contributions(team_drive_id):
    dparser = D_Parser(file_revisions)


@route('/main')
def main():
    return request_list_all_users()


@route('/logout')
def logout():
    service = None
    os.remove('token.json')
    return redirect('/')

run(host='localhost', port=7878)
