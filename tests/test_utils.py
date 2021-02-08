from datetime import date

import pytest

from utils import string_to_date


@pytest.mark.utils
def test_string_to_date():
    assert string_to_date('2020-01-01', '%Y-%m-%d') == date(2020, 1, 1)
