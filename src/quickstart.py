from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
            # rev = service.revisions().list(
            #     fileId=item['id'], fields="*").execute()

            # print(rev.get('revisions', []))

    # response = service.changes().getStartPageToken().execute()
    # print('Start token: %s' % response.get('startPageToken'))

    # # Begin with our last saved start token for this user or the
    # # current token from getStartPageToken()
    # page_token = response.get('startPageToken')
    # while page_token is not None:
    #     response = service.changes().list(
    #         pageToken=page_token, spaces='drive').execute()
    #     print(response)
    #     for change in response.get('changes'):
    #         # Process change
    #         print('Change found for file: %s' % change.get('fileId'))
    #     if 'newStartPageToken' in response:
    #         # Last page, save this token for the next polling interval
    #         saved_start_page_token = response.get('newStartPageToken')
    #         page_token = response.get('nextPageToken')

if __name__ == '__main__':
    main()
