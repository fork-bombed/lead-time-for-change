import os, sys, inspect
from os import path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
srcDir = path.join(parentdir, "src")
print(parentdir, srcDir)
sys.path.insert(0, parentdir)
sys.path.insert(0, srcDir)
print(sys.path)

from commit import Commit
import pytest
import requests
import yaml
from datetime import datetime

'''Tests the Commit class
=======================================================
    Commit class takes a json object to initiate it. And then it has one function get_date. 
    To test this class, we shall pass None, a bad json object and a correct json object to know 
    if all cases are handled properly.  
'''

DUMMY_COMMIT_RESPONSE_DICT = {"commit": {"committer": {}}}

EXPECTED_DATE_STRING = '2021-01-17T09:11:55Z'
EXPECTED_DATE = datetime.strptime(EXPECTED_DATE_STRING, "%Y-%m-%dT%XZ")
CORRECT_COMMIT_RESPONSE_DICT = {"commit": {"committer": {"date": EXPECTED_DATE_STRING}}}

@pytest.mark.parametrize(
    'data, expected_date, is_pass',
    [
        (CORRECT_COMMIT_RESPONSE_DICT, EXPECTED_DATE, True),  # Pass
        (DUMMY_COMMIT_RESPONSE_DICT, None, False),  # expected date doesn't matter

        # expected date doesn't matter. Attribute error
        # because None of .items() is not possible
        ({}, None, False),
    ]
)
def test_commit(data, expected_date, is_pass):
    if not is_pass:
        with pytest.raises(Exception) as e_info:  # Expecting an exception
            commit = Commit(data)
            commit.get_date()
    else:  # Shouldn't get an exception
        commit = Commit(data)
        assert commit.get_date() == expected_date, "Date or the format did not match " \
                                                        "the expected date: %s" % expected_date
