import os, sys, inspect
from os import path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
srcDir = path.join(parentdir, "ltfc")
print(parentdir, srcDir)
sys.path.insert(0, parentdir)
sys.path.insert(0, srcDir)
print(sys.path)

from release import Release
import pytest
import requests
import yaml
from datetime import datetime

'''Tests the Release class
=======================================================
    Release class takes session and a json object containing release info. 
    session will be passed as it is from the session variable because 
    github api is separately tested and we assume its working fine. 
    
    The release object needs the following properties to allow Release class 
    to function properly:
    1. tag_name
    2. created_at
    3. url
    
    We shall pass the correct object and see if the functions return right values. 
    Additionally, we will verify if update of release note is happening properly. 
    
 
'''




session = requests.Session()


EXPECTED_DATE_STRING = '2021-01-17T09:11:55Z'
EXPECTED_DATE = datetime.strptime(EXPECTED_DATE_STRING, "%Y-%m-%dT%XZ")
DATA_OBJECT = {"created_at": EXPECTED_DATE_STRING,
               "url": "latest_release['url']", 'tag_name': "sample_tagname"}

def test_release():
    release = Release(session, DATA_OBJECT)
    assert release.get_tag_name() == DATA_OBJECT['tag_name'], "get_tag_name output did not match"
    assert release.get_creation_time() == EXPECTED_DATE, "get_creation_time output did not match"
    #message = "Test release"
    #release.update(message)
    #all_releases = session.get(REPO_RELEASE_URL).json()
    #latest_release = all_releases[0]
    #assert latest_release['body'] == message, "Release updated message did not match"
