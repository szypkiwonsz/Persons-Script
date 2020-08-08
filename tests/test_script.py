from argparse import Namespace

import pytest

from script import *


def test_database_file_exist():
    assert database_file_exist('not_existing_path') == False


def test_check_if_arguments():
    assert check_if_arguments(Namespace(a='0')) == True
    assert check_if_arguments(Namespace(a='1', b='0', c='argument')) == True
    assert check_if_arguments(Namespace()) == False


def test_get_api_url():
    assert get_api_url(25) == 'https://randomuser.me/api/?results=25'
    assert get_api_url('25') == 'https://randomuser.me/api/?results=25'


def test_load_data_api_check_argument():
    with pytest.raises(Exception):
        load_data_api_check_argument(0)
    with pytest.raises(Exception):
        load_data_api_check_argument('string')
    with pytest.raises(Exception):
        load_data_api_check_argument(5001)
    assert load_data_api_check_argument(5000) == 5000


# def test_main_load_data_api(capfd):
#     os.system('python ./persons/script.py "-load-data-api"')
#     no_argument = capfd.readouterr()
#     os.system('python ./persons/script.py "-load-data-api" -1')
#     negative_number = capfd.readouterr()
#     os.system('python ./persons/script.py "-load-data-api" 5001')
#     too_large_number = capfd.readouterr()
#     os.system('python ./persons/script.py "-load-data-api" 2 2')
#     invalid_number_of_arguments = capfd.readouterr()
#     os.system('python ./persons/script.py "-load-data-api" random')
#     string_argument = capfd.readouterr()
#     print(no_argument.err)
#     assert no_argument.err == 'usage: script.py [-h] [-load-data-api N]\r\nscript.py: error: argument ' \
#                               '-load-data-api: expected one argument\r\n'
#     assert negative_number.err == 'usage: script.py [-h] [-load-data-api N]\r\nscript.py: error: argument ' \
#                                   '-load-data-api: Argument has to be an int from 1 to 5000\r\n'
#     assert too_large_number.err == 'usage: script.py [-h] [-load-data-api N]\r\nscript.py: error: argument ' \
#                                    '-load-data-api: Argument has to be an int from 1 to 5000\r\n'
#     assert invalid_number_of_arguments.err == 'usage: script.py [-h] [-load-data-api N]\r\nscript.py: error: ' \
#                                               'unrecognized arguments: 2\r\n'
#     assert string_argument.err == 'usage: script.py [-h] [-load-data-api N]\r\nscript.py: error: argument ' \
#                                   '-load-data-api: Argument has to be an int from 1 to 5000\r\n'
