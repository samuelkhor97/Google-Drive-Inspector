"""
@author: Samuel, Tiong
@since: 25/8/2018
@modified: 28/9/2018

"""
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient import errors
from d_parser import D_Parser
import time


def getRevisionsForFile(drive_file, service):
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
        pass

    return file_revisions


def getDriveIds(service):
    """
    Call the Drive v3 API to get the teamDrive Ids and bind them with their
    corresponding names in dict

    @:service: (class) The Google Drive service built
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


def listFilesForTeamDrive(team_drive_id, service):
    """
    Get the list of files in of a particular team_drive in team_drives_dict and bind them to their corresponding
    teamDrive Id in a dict

    @:param team_drive: (String) Name for a Team Drive
    @:return team_drive_files: (dictionary) {key:team_drive_id, value:list of Files resources}
    @pre-condition: Google Drive API v3 'service' initialized
    """

    team_drive_files = {}
    key = team_drive_id
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


def get_file_revisions(drive_id, service):
    """
    Get the file_revisions
    @:service: (class) The Google Drive service built
    @:return file_revisions: (dict) File revisions
    """

    # Get the list of files in the teamDrive with 'drive_id' and bind them to its 'drive_id'
    # team_drive_files: {'team_drive_id':list of Files resources}
    team_drive_files = listFilesForTeamDrive(drive_id, service)

    # Get the list of revisions for each file and bind them to their corrsponding
    # file_id
    # file_revisions: {'file_id':list of Revisions resources,....}
    start = time.time()
    file_revisions = {}
    # Only one key-value pair in the dict, hence assessing the only value this
    # way
    team_drive_id = next(iter(team_drive_files))

    for drive_file in team_drive_files[team_drive_id]:
        # Merge the previous file_revisions with new file_revisions from getRevisionsForFile()
        # in every loop
        file_revisions = {**file_revisions, **getRevisionsForFile(drive_file, service)}

    end = time.time()
    print('time elapsed for getting team_drive_files: ' + str(end - start))

    for i in file_revisions:
        break

    return file_revisions
