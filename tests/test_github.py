import os,sys,inspect
from os import path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
srcDir = path.join(parentdir, "ltfc")
print(parentdir, srcDir)
sys.path.insert(0,parentdir)
sys.path.insert(0,srcDir)
print(sys.path)

from github import Github
import pytest
import yaml

'''Tests the Github class
=======================================================
   

'''

def test_get_repository():
    try:
        github = Github('token', 'base_url')
        github.get_repository('repo_name')
    except:
        pass

