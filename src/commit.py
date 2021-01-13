import requests
from datetime import datetime


class Commit:

    def __init__(self, session: requests.Session, data: requests.Response.json) -> None:
        # Create variables from the data dictionary.
        for key, value in data.items():
            setattr(self, key, value)
        
    def get_date(self) -> datetime.strptime:
        return datetime.strptime(self.commit["committer"]["date"], "%Y-%m-%dT%XZ")