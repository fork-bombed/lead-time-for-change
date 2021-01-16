import json

import requests


class Release:

    def __init__(self, session: requests.Session, data: requests.Response.json) -> None:
        self.__session = session

        # Create variables from the data dictionary.
        for key, value in data.items():
            # In order to create a private variable through setattr then we have to also use the class name. 
            # Valid Example: __Release__release
            # Invalid Example: __release
            setattr(self, f"_{self.__class__.__name__}__{key}", value)

    def get_creation_time(self) -> str:
        return self.__created_at

    def get_tag_name(self) -> str:
        return self.__tag_name

    def update(self, message: str) -> None:
        self.__session.patch(
            url=self.__url,
            data=json.dumps({"body": message})
        )
