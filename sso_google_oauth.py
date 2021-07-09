#! /usr/bin/env python
"""
A Flask app for Google SSO
"""

import json
import requests
from flask import Flask, redirect, request
from  oauthlib import oauth2
import conf

CLIENT_ID = conf.CLIENT_ID
CLIENT_SECRET = conf.CLIENT_SECRET

DATA = {
        'response_type':"code",
        'redirect_uri':"https://localhost:5000/home",
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'client_id':CLIENT_ID,
        'prompt':'consent'}

URL_DICT = {
        # Google OAuth URI
        'google_oauth' : 'https://accounts.google.com/o/oauth2/v2/auth',
        # URI to generate token to access Google API
        'token_gen' : 'https://oauth2.googleapis.com/token',
        # URI to get the user info
        'get_user_info' : 'https://www.googleapis.com/oauth2/v3/userinfo'
        }


CLIENT = oauth2.WebApplicationClient(CLIENT_ID)
REQ_URI = CLIENT.prepare_request_uri(
    uri=URL_DICT['google_oauth'],
    redirect_uri=DATA['redirect_uri'],
    scope=DATA['scope'],
    prompt=DATA['prompt'])

app = Flask(__name__)

@app.route('/')
def login():
    "Home"

    return redirect(REQ_URI)

@app.route('/home')
def callback():
    "Redirect after Google login & consent"

    # Get the code after authenticating from the URL
    code = request.args.get('code')

    # Generate URL to generate token
    token_url, headers, body = CLIENT.prepare_token_request(
            URL_DICT['token_gen'],
            authorisation_response=request.url,
            # request.base_url is same as DATA['redirect_uri']
            redirect_url=request.base_url,
            code=code)

    # Generate token to access Google API
    token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(CLIENT_ID, CLIENT_SECRET))

    # Parse the token response
    CLIENT.parse_request_body_response(json.dumps(token_response.json()))

    # Add token to the  Google endpoint to get the user info
    # oauthlib uses the token parsed in the previous step
    uri, headers, body = CLIENT.add_token(URL_DICT['get_user_info'])

    # Get the user info
    response_user_info = requests.get(uri, headers=headers, data=body)
    info = response_user_info.json()

    return redirect('/user/%s' % info['name'])

@app.route('/user/<name>')
def landing_page(name):
    "Landing page after successful login"

    return "Hello %s" % name

if __name__ == '__main__':
    app.run(debug=True, port=5000, ssl_context='adhoc')
