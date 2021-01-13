import requests
import json


class Release:

    def __init__(self, session: requests.Session, data: requests.Response.json) -> None:
        self.__session = session

        # Create variables from the data dictionary.
        for key, value in data.items():
            setattr(self, key, value)

    def get_tag_name(self) -> str:
        return self.tag_name

    def update(self, message: str) -> None:
        self.__session.patch(
            url=self.url,
            data=json.dumps({"body": message})
        )
