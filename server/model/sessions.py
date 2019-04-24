from uuid import uuid1
from datetime import datetime

MAX_SESSION_AGE = 60  # seconds


class Session():
    def __init__(self, ip_addr: str, username: str):
        self.session_id = uuid1()
        self.created = datetime.utcnow().timestamp()
        self.ip_addr = ip_addr
        self.username = username

    def to_dict(self) -> dict:
        return {
            'session_id' : self.session_id,
            'created' : self.created,
            'ip_addr' : self.ip_addr,
            'username' : self.username
        }

