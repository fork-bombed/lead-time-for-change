import requests
from release import Release
from commit import Commit


class Repository:
    
    def __init__(self, session: requests.Session, data: requests.Response.json) -> None:
        self.__session = session

        # Create variables from the data dictionary.
        for key, value in data.items():
            # In order to create a private variable through setattr then we have to
            # also use the class name. 
            # Valid Example: _Repository__repository
            # Invalid Example: __repository
            setattr(self, f"_{self.__class__.__name__}__{key}", value)

    def get_commits(self) -> requests.Response.json:
        response = self.__session.get(
            url=self.__commits_url.replace("{/sha}", "")
        )
        # TODO: Handle exception where a release doesn't exist.
        return [Commit(session=self.__session, data=data) for data in response.json()]

    def get_releases(self) -> requests.Response.json:
        response = self.__session.get(
            url=self.__releases_url.replace("{/id}", "")
        )
        # TODO: Handle exception where a release doesn't exist.
        return response.json()

    def get_latest_release(self) -> Release:
        response = self.__session.get(
            url=self.__releases_url.replace("{/id}", "/latest")
        )
        # TODO: Handle exception where a release doesn't exist.
        return Release(session=self.__session, data=response.json())
