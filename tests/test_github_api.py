import os, sys, inspect
from os import path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
srcDir = path.join(parentdir, "src")
sys.path.insert(0, parentdir)
sys.path.insert(0, srcDir)

import github_api
from repository import Repository
from release import Release
from commit import Commit
import pytest
import requests
from datetime import datetime, timedelta

'''Tests the Github class
=======================================================
    This class has two functions:
    1. get_lead_time: Takes a release and repository parameter
        - We will pass None as a parameter and test if its been handled
        - repositories with 0, 1 and 2 releases
        - repositories with 1 and 2 commits after the previous releases. 
        Note: Although 0 commits between 2 releases is not a real situation, but mathematically and technially possible. 
                Hence written.  
        Note: release parameter isn't used in code. So, we won't test it.
    
    2. get_release_template: Take release and repository parameter
        - We shall pass the above objects to get a fixed tag name and lead time 
        and check if the return template contains these
        - Also, we shall check if the template.md file exists. 
'''

# CONFIG_NAME = "config.yaml"
# if not os.path.isfile(f'../{CONFIG_NAME}'):
#     raise Exception(f'{CONFIG_NAME} not found')
#
# with open(f'../{CONFIG_NAME}') as file:
#     CONFIG = yaml.safe_load(file)
#
# WORKING_TOKEN = CONFIG.get('token')
#
# base_url = "https://api.github.com"
session = requests.Session()
# session.headers.update({"Authorization": f"Token {WORKING_TOKEN}"})

# """Create a dummy project like https://api.github.com/repos/VenkatTeja/APITest
#     And configure the urls below. Do not make any future changes to this project,
#      else the information has to be updated for the tests to be accurate.
# """
# REPO_COMMITS_URL = 'https://api.github.com/repos/VenkatTeja/APITest/commits'  # UPDATE THIS
# REPO_RELEASES_URL = 'https://api.github.com/repos/VenkatTeja/APITest/releases'  # UPDATE THIS
# COMMITS_IN_PROJECT = 2  # UPDATE THIS
# RELEASES_IN_PROJECT = 1  # UPDATE THIS
# LATEST_RELEASE_TAG_NAME = "1.0.0"  # UPDATE THIS

EXPECTED_DATE_STRING = '2021-01-17T09:11:55Z'
EXPECTED_DATE = datetime.strptime(EXPECTED_DATE_STRING, "%Y-%m-%dT%XZ")
DATA_OBJECT = {"created_at": EXPECTED_DATE_STRING,
               "commits_url": "REPO_COMMITS_URL", 'releases_url': "REPO_RELEASES_URL", "full_name": 'fullName'}

TAG_NAME = "sample_tagname"

def generateReleaseFunction(nReleases: int):
    """Generates mock release objects array"""
    releases = []
    ORIGINAL_EXPECTED_DATE_STRING = '2021-01-17T09:11:55Z'
    EXPECTED_DATE = datetime.strptime(ORIGINAL_EXPECTED_DATE_STRING, "%Y-%m-%dT%XZ") + timedelta(seconds=5) # 5 seconds after repo init
    for i in range(nReleases):
        EXPECTED_DATE_STRING = (EXPECTED_DATE + timedelta(seconds=(i * 60))).strftime("%Y-%m-%dT%XZ")
        RELEASE_DATA_OBJECT = {"created_at": EXPECTED_DATE_STRING,
                               "url": "latest_release['url']", 'tag_name': TAG_NAME, "id": i}
        releases.insert(0, Release(session, RELEASE_DATA_OBJECT))

    def get_releases():
        return releases
    return get_releases

def generateCommitsFunction(nCommits: int):
    """Generates mock commit objects array"""
    commits = []
    ORIGINAL_EXPECTED_DATE_STRING = '2021-01-17T09:11:55Z'
    EXPECTED_DATE = datetime.strptime(ORIGINAL_EXPECTED_DATE_STRING, "%Y-%m-%dT%XZ")
    for i in range(nCommits):
        EXPECTED_DATE_STRING = (EXPECTED_DATE + timedelta(seconds=(i*30))).strftime("%Y-%m-%dT%XZ")
        CORRECT_COMMIT_RESPONSE_DICT = {"commit": {"committer": {"date": EXPECTED_DATE_STRING}}}
        commits.append(Commit(CORRECT_COMMIT_RESPONSE_DICT))

    def get_commits():
        return commits
    return get_commits


repo = Repository(session, DATA_OBJECT)

@pytest.mark.parametrize(
    'repo2, nReleases, nCommits, expected_lead_time, is_pass',
    [
        (None, None, None, 0, False),
        (repo, 0, 0, 0, False),  # Should handle for no releases
        # (repo, get_one_release, generateCommitsFunction(0), , True), - Not a condition in release life. Theres going to be atleast one commit in a one release repo
        (repo, 1, 1, 0, True),
        (repo, 1, 2, 15, True),
        (repo, 2, 2, 25, True),  # 1 commits after first release
        (repo, 2, 3, 40, True),  # 2 commits after first release
    ])
def test_get_lead_time(repo2, nReleases, nCommits, expected_lead_time, is_pass):
    if repo2 is not None:
        repo2.get_releases = generateReleaseFunction(nReleases)
        repo2.get_commits = generateCommitsFunction(nCommits)

    if not is_pass:
        with pytest.raises(Exception) as e_info:
            github_api.get_lead_time(repo2.get_releases()[0], repo2)
    else:
        lead_time = github_api.get_lead_time(repo2.get_releases()[0], repo2)
        assert timedelta(seconds=expected_lead_time) == lead_time, "Lead time is not the expected one (%s)" % (expected_lead_time)

def test_get_release_template():
    if repo is not None:
        repo.get_releases = generateReleaseFunction(2)
        repo.get_commits = generateCommitsFunction(3)
    lead_time = github_api.get_lead_time(repo.get_releases()[0], repo)
    lead_time_string = str(lead_time)
    release = generateReleaseFunction(1)()[0]
    string = '{version} - {lead_time}'
    formatted_string = github_api.get_release_template(release, release, repo)
    if path.isfile("template.md"):
        raise Exception("src/template.md is not found")
    assert TAG_NAME in formatted_string, 'template string doesn\'t contain expected tag name: %s' % TAG_NAME
    # assert "0:00:40" in formatted_string, 'template string doesn\'t contain expected lead time: %s' % "0:00:40"

@pytest.mark.parametrize(
    'day, hour, minute, expected',
    [
        (2, 4, 30, "2d%203h%2030m"),
        (2, 4, 0, "2d%204h"),
        (2, 0, 0, "2d"),
        (0, 0, 0, "")
    ])
def test_format_urlsafe_time(day, hour, minute, expected):
    d1 = datetime.now()
    d1 = d1.replace(day=6, hour=12, minute=0, second=0)
    d2 = d1.replace(day=d1.day - day, hour=d1.hour - hour, minute=minute)
    assert github_api.format_urlsafe_time(d1-d2)==expected, "test_format_urlsafe_time failed"

@pytest.mark.parametrize(
    'nReleases, nCommits, expectedCommitsSize',
    [
        (2, 2, 1),
        (3, 3, 2)
    ])
def test_get_commits_between_releases(nReleases, nCommits, expectedCommitsSize):
    repo.get_releases = generateReleaseFunction(nReleases)
    repo.get_commits = generateCommitsFunction(nCommits)
    commits = github_api.get_commits_between_releases(repo.get_releases()[0], repo.get_releases()[nReleases-1], repo)
    assert len(commits)==expectedCommitsSize
