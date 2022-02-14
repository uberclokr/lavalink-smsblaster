#!/usr/bin/python
import requests
import pickle
import base64
import json
import os
import config

goto_session_filename = 'goto_auth_session'

class GoToClient:

    def __init__(self):

        self.goto_auth_session = refresh_session(get_access_token(get_auth_code())) # Refresh session at init in case the current one is expired

    def send_sms(self, message: str, recipient: str):

        # Send an SMS
        """
        NOTE
        - Adding more than one recipient at a time will make this a GROUP message
        
        EXAMPLE CURL
        curl -X "POST" "https://api.jive.com/messaging/v1/messages" \
        -H "Content-Type: application/json" \
        -d '{"ownerPhoneNumber": "+15551234567", "contactPhoneNumbers": [ "+15559998888" ], "body": "Hi Bob!"}' \
        -H 'Authorization: Bearer {token}'
        """

        url = 'https://api.jive.com/messaging/v1/messages'
        jive_messages_headers = {
            'Content-Type': 'application/json',
            'Authorization': f"{self.goto_auth_session['token_type']} {self.goto_auth_session['access_token']}"
        }
        jive_messages_data = { # Data ultimately needs to be converted to a string before sending
            'ownerPhoneNumber': config.jive_owner_phone,
            'contactPhoneNumbers': [recipient],
            'body': message
        }

        r = requests.post(url, headers=jive_messages_headers, data=json.dumps(jive_messages_data))

        return r.status_code

def get_auth_code():

    # Obtain authorization code if goto_auth_session does not exist
    goto_auth_code = None

    if not os.path.exists(goto_session_filename):

        try:
            with open('goto_auth_code', 'rb') as pickle_file:
                goto_auth_code = pickle.load(pickle_file)

        except:
            print(f"""
                For first time execution, you will need to request application access by navigating to this URL in a web browser:
                {config.goto_auth_url}

                Upon successful authentication, you will be redirected to {config.goto_redirect_uri}.
                
            """)
            goto_auth_code = input('Please provide the code GET variable from your resulting redirect URL here:')
            with open('goto_auth_code', 'wb') as pickle_file:
                pickle.dump(goto_auth_code,pickle_file)

    return goto_auth_code

def get_access_token(auth_code):

    # Establish session by obtaining access token
    """ WORKING EXAMPLE CURL
    curl -X POST "https://api.getgo.com/oauth/v2/token" \
    -H "Authorization: Basic MjZkYzczOWUtOWIzMi00ZGEyLTk2YmYtZTM2NDYwNDYwMTQ4Ok9uMDU3TjN6ZnZmSk1oUTk0NWdLNU9RYg==" \
    -H "Accept:application/json" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "redirect_uri=https://lavalink.us&grant_type=authorization_code&code=eyJraWQiOiJvYXV0aHYyLmxtaS5jb20uMDIxOSIsImFsZyI6IlJTNTEyIn0.eyJzYyI6ImNhbGwtY29udHJvbC52MS5jYWxscy5jb250cm9sIGNhbGxzLnYyLmluaXRpYXRlIGNyLnYxLnJlYWQgbWVzc2FnaW5nLnYxLm5vdGlmaWNhdGlvbnMubWFuYWdlIG1lc3NhZ2luZy52MS5yZWFkIG1lc3NhZ2luZy52MS5zZW5kIG1lc3NhZ2luZy52MS53cml0ZSByZWFsdGltZS52Mi5ub3RpZmljYXRpb25zLm1hbmFnZSB1c2Vycy52MS5saW5lcy5yZWFkIHdlYnJ0Yy52MS5yZWFkIHdlYnJ0Yy52MS53cml0ZSIsInN1YiI6IjU5MDEyNjUxMjE5MzMzNDM0OTMiLCJhdWQiOiIyNmRjNzM5ZS05YjMyLTRkYTItOTZiZi1lMzY0NjA0NjAxNDgiLCJvZ24iOiJwd2QiLCJscyI6ImZkNThlZmUwLTMzMmUtNGQwMi1hZDQ3LWUzZjdkNjYwMjA0YSIsInR5cCI6ImMiLCJleHAiOjE2NDQxNzU1MzAsImlhdCI6MTY0NDE3NDkzMCwidXJpIjoiaHR0cHM6XC9cL2xhdmFsaW5rLnVzIiwianRpIjoiYTdkYjFiNjYtYjRhNS00NWFhLThmNDUtYTVjM2QwNzI2MDUxIn0.TPp4GsVzfp7E2w4L7JSMT9kBWct0_VC0eEMCfc5PpTrwwruOVPtNNEf8wsO9RMfcP87KMfst1u0-4nFRXcCvYEGHpclYlPFP1qTPE6ozxo9BeUqhqZNGntsbkP298YFyL2R08TvDJbz96I5lcuT_V3lmyarB4YjJ5Gs5KlBIoASeq1s5RmR3diDaiChqJ9Pqar7rn6_7CrDOCH_FfLSNhl9m6oY1DDOI1zl5EliuQUhMt_cnf7d91a9rcGdi5L_pYoRIVVVYEnNBgUYrTZreO33fs2WGi0G5vA84bK28ENmwoQpvdaW-LAgBu84M1mq4SV1vs8Rh8OLpp5zeEsYAZQ"
    """
    try:
        with open(goto_session_filename, 'rb') as pickle_file: # If session file exists, load it
            goto_auth_session = pickle.load(pickle_file)
    except:
        print('Existing session not found. Obtaining new auth token...')
        auth = f'{config.goto_client_id}:{config.goto_client_secret}'
        auth_bytes = auth.encode('utf-8')
        goto_authorization = base64.b64encode(auth_bytes).decode('utf-8')

        goto_access_headers = {
            'Authorization': f'Basic {goto_authorization}',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        goto_access_data = f"redirect_uri={config.goto_redirect_uri}&grant_type=authorization_code&code={auth_code}"
        r = requests.post(config.goto_access_url,headers=goto_access_headers,data=goto_access_data)

        goto_auth_session = r.json()

        if 'error_description' in goto_auth_session:
            print(f"{goto_auth_session['error'].upper()}: {goto_auth_session['error_description']}")
            quit()
        else:
            with open(goto_session_filename, 'wb') as pickle_file:
                pickle.dump(goto_auth_session,pickle_file)

            # goto auth code is no longer valid, discard the file
            os.remove('goto_auth_code')

    return goto_auth_session

def refresh_session(session):

    # Refresh session using refresh token from previously established session

    """ EXAMPLE CURL
    curl --request POST 'https://api.getgo.com/oauth/v2/token' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --header 'Authorization: Basic YTIwfAKeNGYtODY4YS00MzM5LTkzNGYtNGRhMmQ3ODhkMGFhOjNuYU8xMElBMmFnY3ZHKzlJOVRHRVE9PQ==' \
    -d 'grant_type=refresh_token&refresh_token=eyJraWQiOiJvYXV0aHYyLmxt999...'
    """
    try:
        with open(goto_session_filename, 'rb') as pickle_file: # If session file exists, load it
            session = pickle.load(pickle_file)
    except:
        print('Could not load existing session file to refresh token. Please re-attempt initial authentication.')
        quit()

    auth = f'{config.goto_client_id}:{config.goto_client_secret}'
    auth_bytes = auth.encode('utf-8')
    goto_authorization = base64.b64encode(auth_bytes).decode('utf-8')

    goto_access_headers = {
        'Authorization': f'Basic {goto_authorization}',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    goto_access_data = f"grant_type=refresh_token&refresh_token={session['refresh_token']}"
    
    r = requests.post(config.goto_access_url,headers=goto_access_headers,data=goto_access_data)
    session = r.json()

    if 'error_description' in session:
        print(f"{session['error'].upper()}: {session['error_description']}")
        quit()
    else:
        with open(goto_session_filename, 'wb') as pickle_file:
            pickle.dump(session,pickle_file)

    return session