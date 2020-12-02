import pytest
import src.github_api as gh
from datetime import datetime

class TestGetLastModifiedDate:
    
    def test_get_last_modified_date(self):
        date_str = 'Wed, 18 Nov 2020 10:24:29 GMT'
        assert gh.get_last_modified_date(date_str).strftime('%a, %d %b %Y %H:%M:%S')  == 'Wed, 18 Nov 2020 10:24:29'

    def test_get_last_modified_date_exception(self):
        date_str = 'Wed, 18 11 2020 10:24:29 GMT'
        with pytest.raises(ValueError):
            gh.get_last_modified_date(date_str)


