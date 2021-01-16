import json

import requests

from repository import Repository


class Github:
    __username = None
    __base_url = "https://api.github.com"
    __session = requests.Session()

    def __init__(self, token: str) -> None:
        self.__session.headers.update({"Authorization": f"Token {token}"})
        self.__check_token()

    def __check_token(self) -> None:
        response = self.__session.get(self.__base_url + "/user")

        if ("message" in response.json() and
                response.json()["message"] == "Bad credentials"):
            raise ValueError("The GitHub token provided is invalid.")

        self.__username = response.json()["login"]

    def get_repository(self, repo_name: str) -> Repository:
        response = self.__session.get(
            url=f"{self.__base_url}/repos/{self.__username}/{repo_name}"
        )

        if ("message" in response.json() and
                response.json()["message"] == "Not Found"):
            raise ValueError("The repository specified does not exist.")

        return Repository(session=self.__session, data=response.json())
