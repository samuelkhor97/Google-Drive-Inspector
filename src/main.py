"""
@author: Samuel
@since: 25/8/2018
@modified: 16/9/2018

"""
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient import errors
from d_parser import D_Parser
import traceback
import sys
import time

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))


def getRevisionsForFile(drive_file):
    """
    Call the Drive v3 API to get the revision(s) of each file and bind them into to their corresponding
    file in a dict

    @:param drive_file: (dict) A dict containing metadata of a File
    @:return file_revisions: (dictionary) {key:file_id, value:list of Revisions resources}
    @pre-condition: Google Drive API v3 'service' initialized
    @Exception HttpError: (errors) Exception raised when Revisions not supported for a specific file
    """

    file_revisions = {}

    try:
        key = drive_file['id']
        # List of revisions for each file
        file_revisions_list = service.revisions().list(fileId=key, fields='*').execute()
        # add list of revisions for each file into files_revisions dict
        file_revisions[key] = file_revisions_list.get('revisions')

    except errors.HttpError as e:
        # print(str(e))
        # print(traceback.format_exc())
        pass
    # for i in files_revisions:
        # print("file id: " + i)
        # print(files_revisions[i][0]['modifiedTime'])
    return file_revisions


def getDriveIds():
    """
    Call the Drive v3 API to get the teamDrive Ids and bind them with their
    corresponding names in dict

    @:return team_drives_dict: (dictionary) {key:team_drive_name, value:team_drive_id}
    @pre-condition: Google Drive API v3 'service' initialized
    """
    team_drives_dict = {}
    # All the teamdrives resources accessible by the current logged in account
    team_drive_results = service.teamdrives().list().execute()
    # List of all the team drives
    team_drives = team_drive_results.get('teamDrives', [])
    # Loop through every team_drive and add key-value pair of {team_drive_name:team_drive_id}
    # into dict
    for team_drive in team_drives:
        team_drives_dict[team_drive.get('name')] = team_drive.get('id')

    return team_drives_dict


def listFilesForTeamDrive(team_drive, team_drives_dict):
    """
    Get the list of files in of a particular team_drive in team_drives_dict and bind them to their corresponding
    teamDrive Id in a dict

    @:param team_drive: (String) unique Id for each Team Drive
    @:param team_drives_dict: (dictionary) {key:team_drive_name, value:team_drive_id}
    @:return team_drive_files: (dictionary) {key:team_drive_id, value:list of Files resources}
    @pre-condition: Google Drive API v3 'service' initialized
    """

    team_drive_files = {}

    key = team_drives_dict[team_drive]
    # All the Files resources for the particular team_drive
    team_drive_file_list = service.files().list(corpora='teamDrive', includeTeamDriveItems=True,
                                                supportsTeamDrives=True,
                                                q=("mimeType='application/vnd.google-apps.document'" or
                                                   "mimeType=application/vnd.google-apps.spreadsheet'" and
                                                   "trashed='False'"),
                                                teamDriveId=key).execute()
    # Add key-value pair of {team_drive_id:list of Files resources} into dict
    team_drive_files[key] = team_drive_file_list.get('files')

    return team_drive_files


def get_file_revisions():
    """
    Get the file_revisions
    @:return file_revisions: (dict) File revisions
    """
    # Get team drives Id and names
    # team_drives_dict: {'team_drives_names':'team_drive_id',........}
    team_drives_dict = getDriveIds()
    # print(team_drives_dict)

    # Get the list of files in each teamDrive and bind them to their corresponding
    # teamDrive Id in a dict
    # team_drive_files: {'team_drive_id':list of Files resources,.....}
    team_drive_files = {}
    for team_drive in team_drives_dict:
        # Merge the previous team_drive_files with new team_drive_files from
        # listFilesForTeamDrive() in every loop
        team_drive_files = {**team_drive_files, **listFilesForTeamDrive(team_drive, team_drives_dict)}

   # print(team_drive_files)

    # Get the list of revisions for each file and bind them to their corrsponding
    # file_id
    # file_revisions: {'file_id':list of Revisions resources,....}
    start = time.time()
    file_revisions = {}
    for team_drive_id in team_drive_files:
        for drive_file in team_drive_files[team_drive_id]:
            # Merge the previous file_revisions with new file_revisions from getRevisionsForFile()
            # in every loop
            file_revisions = {**file_revisions, **getRevisionsForFile(drive_file)}

    end = time.time()
    print('time elapsed for getting team_drive_files: ' + str(end - start))

    for i in file_revisions:
        # print(i, file_revisions[i])
        break
    return file_revisions


def main():
    file_revisions = get_file_revisions()

    dparser = D_Parser(file_revisions)
    for file_id in file_revisions:
        print(file_id, end='')
        # print(dparser.calculate_file_contribution(file_id))
        print(dparser.calculate_total_contribution_within_timeframe(
            '2018-05-19', '2018-05-20'))

        break
    sys.exit(0)
    print(dparser.calculate_total_contribution())
    print(dparser.calculate_total_contribution_percentage())
    print(dparser.calculate_total_contribution_with_week())

    for file_id in file_revisions:
        dparser.print_revisions_user(file_id)


def WIP_request_handler():
    file_revisions = get_file_revisions()
    dparser = D_Parser(file_revisions)
    return_string = ""

    for file_id in file_revisions:
        return_string += str.join('<br />',
                                  dparser.list_revisions_user(file_id)) + '<hr />'

    return return_string

if __name__ == '__main__':
    main()
