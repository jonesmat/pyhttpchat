'''
The client app will hit the server api to send and receive chat messages.

Functionality of the client:
    - Create a session on the server.
    - Get a list of other sessions on the server.
    - Send messages to other sessions.
    - Get messages for this client's session.
'''

from typing import List, Optional
import json

from flask import Flask, request, jsonify, redirect, url_for, session, render_template
import requests

app = Flask(__name__)

# TODO Move this to a key store
app.secret_key = b'_5#y5L"F3Q8z\n\xec]/'

BASE_SERVER_URL = "http://127.0.0.1:5000"


@app.route("/")
def index():
    if not session['id']:
        return redirect(url_for('login'))

    vm = {
        "username" : session['username']
    }
    return render_template('index.html', vm=vm)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        r = requests.post(f'{BASE_SERVER_URL}/sessions', data={'username': username})
        print(r.status_code, r.reason)
        
        if (r.status_code == 200):
            responseData = r.json()
            
            session['id'] = responseData["session_id"]
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # It's unlikely we get here without requests or flask raising their own exception
            raise Exception("Unexpected error logging in")
        


