'''
It will do:
- start a local web server (bottle framework)
- load another file that handle web requests
-- that file will call functions from current drive_functions.py
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
import webbrowser

# Add template directory
viewpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))
bottle.TEMPLATE_PATH.insert(0, viewpath)

# Declare global variables used across multiple pages
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
    # If access token not found, prompt for Google sign in,
    # create the token and redirect
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
    # Reinitialize the global variables to default
    global file_revisions
    file_revisions = None

    global current_drive_id
    current_drive_id = None

    global drive_ids
    drive_ids = getDriveIds(service)

    # List all the team drives the user in
    for drive_name in drive_ids:
        drive_ids[drive_name] = '/loading/' + drive_ids[drive_name]

    return template('team_drives', drive_ids=drive_ids)


def load_file_revisions(team_drive_id, service):
    global file_revisions
    file_revisions = get_file_revisions(team_drive_id, service)


@route('/isready')
def isready():
    # Check whether the file_revisions are loaded
    return '1' if file_revisions != None else '0'


@route('/loading/<team_drive_id>')
def loading(team_drive_id):
    # Go to loading page while file_revisions are being fetched
    thr = Thread(target=load_file_revisions, args=[team_drive_id, service])
    thr.start()
    # Redirect to redirect_link after file_revisions been fetched
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
    global file_names_ids_dict
    file_names_ids_dict = get_file_names_ids(team_drive_id)

    global current_drive_id
    current_drive_id = team_drive_id

    # Initialize D_Parser class to calculate overall drive contributions
    dparser = D_Parser(file_revisions)
    all_users_contributions = dparser.calculate_total_contribution()
    all_users_contributions_percentage = dparser.calculate_total_contribution_percentage()
    users_list, all_users_weekly_contributions = dparser.calculate_contribution_with_week()

    # Finding the drive_name in drive_ids dict
    drive_name = list(drive_ids.keys())[list(
        drive_ids.values()).index('/loading/' + str(team_drive_id))]
    return template('team_contributions',
                    drive_name=drive_name,
                    contributions=all_users_contributions,
                    contributions_percent=all_users_contributions_percentage,
                    weekly_contributions=all_users_weekly_contributions,
                    users_list=users_list,
                    file_names_ids=file_names_ids_dict)


@route('/file_contribution/<file_id>')
def file_contribution(file_id):
    # Initialize D_Parser class to calculate individual file contributions
    dparser = D_Parser(file_revisions)
    file_contribution = dparser.calculate_file_contribution(file_id)
    file_contribution_percentage = dparser.calculate_file_contribution_percentage(
        file_id)
    users_list, all_users_weekly_contributions = dparser.calculate_contribution_with_week(
        file_id)
    # Finding the file_name in file_names_ids dict
    file_name = list(file_names_ids_dict.keys())[list(
        file_names_ids_dict.values()).index('/file_contribution/' + str(file_id))]
    return template('file_contribution',
                    current_drive=current_drive_id,
                    file_name=file_name,
                    contribution=file_contribution,
                    contribution_percent=file_contribution_percentage,
                    weekly_contributions=all_users_weekly_contributions,
                    users_list=users_list,
                    file_names_ids=file_names_ids_dict)


@route('/timeContribution/<startDate>/<endDate>/<drive_name>')
def timeframe_contribution(startDate, endDate, drive_name):
    # Initialize D_Parser class to calculate overall drive contributions
    # within a timeframe set by user
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
    # Reinitialize the global variables to initial states and
    # remove the access token from device before logging out
    global service
    service = None
    global file_revisions
    file_revisions = None
    global current_drive_id
    current_drive_id = None

    os.remove('token.json')
    return redirect('/')

if __name__ == "__main__":
    # Open up a default browser tab for the login page
    webbrowser.open('http://localhost:{}'.format(port))
    # Run the program at localhost with predefined port
    run(host='localhost', port=port)
