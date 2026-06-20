import os
import base64

def restore_files():
    token_b64 = os.environ.get('TOKEN_PICKLE_B64')
    creds_b64 = os.environ.get('CREDENTIALS_JSON_B64')

    if token_b64:
        with open('token.pickle', 'wb') as f:
            f.write(base64.b64decode(token_b64))

    if creds_b64:
        with open('credentials.json', 'wb') as f:
            f.write(base64.b64decode(creds_b64))