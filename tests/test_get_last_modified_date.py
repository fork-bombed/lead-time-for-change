import pytest
from github_api import get_last_modified_date
import src.github_api
from datetime import datetime

class TestGetLastModifiedDate:
    
    def test_get_last_modified_date():
        date_str = 'Wed, 18 Nov 2020 10:24:29 GMT'
        assert get_last_modified_date(date_str).strftime('%a, %d %b %Y %H:%M:%S %Z')  == 'Wed, 18 Nov 2020 10:24:29 GMT'

    def test_get_last_modified_date_exception():
        date_str = 'Wed, 18 11 2020 10:24:29 GMT'
        with pytest.raises(ValueError):
            get_last_modified_date(date_str)


