from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import sys
import io
from pprint import pprint
from googleapiclient.http import MediaFileUpload


files = [
        "OCRL/datasets/random/RandomObjsEnv-N5C4S4-AgentPosNo-WoAgentTrue-OcclusionTrue-SkewedFalse-Tr1000000-Val10000.hdf5"
]

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# this is the library object
service = build('drive', 'v3', credentials=creds)

# uploading
for the_file_to_upload in files:
    metadata = {'name': the_file_to_upload, 'parents': ['1RlJXokd2096VCkb6Z8YNTxlDhjFSigGb']}
    media = MediaFileUpload(the_file_to_upload,
        chunksize=5 * 1024 * 1024,
        mimetype='application/octet-stream',
        resumable=True)
    request = service.files().create(body=metadata, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))

    print("Upload of {} is complete.".format(the_file_to_upload))
