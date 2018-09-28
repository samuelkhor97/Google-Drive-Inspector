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
# delete below import later
import webbrowser
# import mpld3
# from graphing_functions import *

# add template directoryb
viewpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))
bottle.TEMPLATE_PATH.insert(0, viewpath)
service = None
file_revisions = None
drive_ids = None
file_names_ids_dict = None
current_drive_id = None
flow = None
port = 7878


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
            'credentials.json', scope=SCOPES,
            redirect_uri='http://localhost:{}/login/return'.format(port))

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
    global file_revisions
    file_revisions = None

    global current_drive_id
    current_drive_id = None

    global drive_ids
    drive_ids = getDriveIds(service)

    for drive_name in drive_ids:
        drive_ids[drive_name] = '/loading/' + drive_ids[drive_name]

    return template('team_drives', drive_ids=drive_ids)


def load_file_revisions(team_drive_id, service):
    global file_revisions
    file_revisions = get_file_revisions(team_drive_id, service)


@route('/isready')
def isready():
    return '1' if file_revisions != None else '0'


@route('/loading/<team_drive_id>')
def loading(team_drive_id):
    thr = Thread(target=load_file_revisions, args=[team_drive_id, service])
    thr.start()
    redirect_link = '/team_drive_contributions/' + team_drive_id
    return template('loading', redirect_link=redirect_link)


def get_file_names_ids(team_drive_id):
    """
    @:return file_names_ids_dict: (dict) {key:file_name(string), 
    value:/file_contribution/file_id, key:...}
    """
    files_list = listFilesForTeamDrive(
        team_drive_id, service)[team_drive_id]

    file_names_ids_dict = {}
    for file in files_list:
        file_names_ids_dict[file['name']] = '/file_contribution/' + file['id']

    return file_names_ids_dict


@route('/team_drive_contributions/<team_drive_id>')
def team_contributions(team_drive_id):
    # dict2 = {"Peak Khor": {"2018week36": 2, "2018week37": 5},
    #          "Clare": {"2018week36": 5, "2018week37": 0}}
    # timeline = mpld3.fig_to_html(timelineChart(dict2))
    global file_names_ids_dict
    file_names_ids_dict = get_file_names_ids(team_drive_id)

    global current_drive_id
    current_drive_id = team_drive_id

    dparser = D_Parser(file_revisions)
    all_users_contributions = dparser.calculate_total_contribution()
    all_users_contributions_percentage = dparser.calculate_total_contribution_percentage()

    drive_name = list(drive_ids.keys())[list(
        drive_ids.values()).index('/loading/' + str(team_drive_id))]
    return template('team_contributions',
                    drive_name=drive_name,
                    contributions=all_users_contributions,
                    contributions_percent=all_users_contributions_percentage,
                    file_names_ids=file_names_ids_dict)


@route('/file_contribution/<file_id>')
def file_contribution(file_id):
    dparser = D_Parser(file_revisions)
    file_contribution = dparser.calculate_file_contribution(file_id)
    file_contribution_percentage = dparser.calculate_file_contribution_percentage(
        file_id)

    file_name = list(file_names_ids_dict.keys())[list(
        file_names_ids_dict.values()).index('/file_contribution/' + str(file_id))]
    return template('file_contribution',
                    current_drive=current_drive_id,
                    file_name=file_name,
                    contribution=file_contribution,
                    contribution_percent=file_contribution_percentage,
                    file_names_ids=file_names_ids_dict)


@route('/timeContribution/<startDate>/<endDate>/<drive_name>')
def timeframe_contribution(startDate, endDate, drive_name):
    dparser = D_Parser(file_revisions)
    time_framed_contribution = dparser.calculate_total_contribution_within_timeframe(
        startDate, endDate)
    time_framed_contribution_percentage = dparser.calculate_total_contribution_within_timeframe_percentage(
        startDate, endDate)
    return template('time_framed_contribution',
                    drive_id=current_drive_id,
                    drive_name=drive_name,
                    start_date=startDate,
                    end_date=endDate,
                    contributions=time_framed_contribution,
                    contributions_percent=time_framed_contribution_percentage)


@route('/logout')
def logout():
    global service
    service = None
    global file_revisions
    file_revisions = None
    global current_drive_id
    current_drive_id = None

    os.remove('token.json')
    return redirect('/')

webbrowser.open('http://localhost:{}'.format(port))

run(host='localhost', port=port)
