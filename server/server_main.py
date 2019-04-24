'''
The server is a hub for clients to send and receive messages.  The server
itself is simply a management tool to moderate, not for typical communication.

Functionality of the server:
    - Allow a user to create a session.
    - See list of active sessions.
    - Ban a session.
    - View chats sent to or received by a session.
    - Send admin messages to a session.
'''

from typing import List, Optional
import json
from datetime import datetime

from flask import Flask, request, jsonify, render_template

from model.sessions import Session, MAX_SESSION_AGE

app = Flask(__name__)

@app.route("/")
def hello():
    vm = {
        "name" : "Matt"
    }
    return render_template('main.html', vm=vm)

### SESSION MGMT ###

_sessions = [] # type: List[Session]

@app.route("/sessions", methods=['GET'])
def sessions_get_all() -> List[Session]:
    return jsonify(eqtls=[session.to_dict() for session in _sessions])

@app.route("/sessions/<username>", methods=['GET'])
def sessions_get_by_username(username: str) -> Session:
    sessions = [session for session in _sessions if session.username == username]
    return jsonify([session.to_dict() for session in sessions])

@app.route("/sessions/", methods=['POST'])
def sessions_create() -> Session:
    '''
    This method allows a user to create a session.  It will return an existing
    if it already exists for their username.
    '''
    ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    username = request.form['username']

    def get_session(username: str) -> Optional[Session]:
        session = None  # type: Optional[Session]
        # Check to see if a session for this user is already active.
        sessions_by_username = [session for session in _sessions if session.username == username]
        print(f'{len(sessions_by_username)} sessions found for username "{username}"')
        
        if len(sessions_by_username) > 0:
            session = sessions_by_username[0]

        # Check to see if the session has expired
        if session:
            session_age = datetime.utcnow().timestamp() - session.created
            if session_age > MAX_SESSION_AGE:
                # Session has expired, remove from Sessions list
                _sessions.remove(session)
                session = None

        return session

    session = get_session(username)

    # If a new session is needed...
    if not session:
        banned = False  # TODO Ensure the user hasn't been banned
        if banned:
            raise Unauthorized("User has been banned")
        
        session = Session(ip_addr, username)
        _sessions.append(session)

    return jsonify(session.to_dict())





### Error Handling ###

class Unauthorized(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(Unauthorized)
def handle_unauthorized_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response