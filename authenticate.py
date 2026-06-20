from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
]

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

with open('token.pickle', 'wb') as f:
    pickle.dump(creds, f)

print("Authentication successful. token.pickle saved.")