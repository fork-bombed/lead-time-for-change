import requests
from release import Release
from commit import Commit


class Repository:
    def __init__(self, session: requests.Session, data: requests.Response.json) -> None:
        self.__session = session

        # Create variables from the data dictionary.
        for key, value in data.items():
            setattr(self, key, value)

    def get_commits(self) -> requests.Response.json:
        response = self.__session.get(
            url=self.commits_url.replace("{/sha}", "")
        )
        # TODO: Handle exception where a release doesn't exist.
        return [Commit(session=self.__session, data=data) for data in response.json()]

    def get_releases(self) -> requests.Response.json:
        response = self.__session.get(
            url=self.releases_url.replace("{/id}", "")
        )
        # TODO: Handle exception where a release doesn't exist.
        return response.json()

    def get_latest_release(self) -> Release:
        response = self.__session.get(
            url=self.releases_url.replace("{/id}", "/latest")
        )
        # TODO: Handle exception where a release doesn't exist.
        return Release(session=self.__session, data=response.json())
