import os, sys, inspect
from os import path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
srcDir = path.join(parentdir, "src")
sys.path.insert(0, parentdir)
sys.path.insert(0, srcDir)

from repository import Repository
import pytest
import requests
import yaml
from datetime import datetime

'''Tests the Repository class
=======================================================
    Repository class takes session and a json object containing Repository info. 
    session will be passed as it is from the session variable because 
    github api is separately tested and we assume its working fine. 

    The Repository object needs the following properties to allow Release class 
    to function properly:
    1. created_at
    2. commits_url
    3. releases_url

    We shall pass the correct object and see if the functions return right values. 
    Additionally, we will verify if update of release note is happening properly.
    
 
'''


session = requests.Session()


EXPECTED_DATE_STRING = '2021-01-17T09:11:55Z'
EXPECTED_DATE = datetime.strptime(EXPECTED_DATE_STRING, "%Y-%m-%dT%XZ")
DATA_OBJECT = {"created_at": EXPECTED_DATE_STRING,
               "commits_url": "REPO_COMMITS_URL", 'releases_url': "REPO_RELEASES_URL"}


def test_repository():
    repo = Repository(session, DATA_OBJECT)
    # assert len(repo.get_commits()) == COMMITS_IN_PROJECT, "Commit's count doesnt match the expected value. " \
    #                                                          "(Remember, the github api may at max fetch 30 commits. " \
    #                                                          "Ensure the configured project has less commits to test"
    assert repo.get_creation_time() == EXPECTED_DATE, "get_creation_time output did not match"

    # assert len(repo.get_releases()) == RELEASES_IN_PROJECT, "Release's count doesn't match the expected value"

    # latest_release = repo.get_latest_release()
    # assert latest_release.get_tag_name() == LATEST_RELEASE_TAG_NAME, "Latest release tag name is not the expected value"

