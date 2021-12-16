
from unittest.mock import patch, mock_open, Mock, call

import pytest

from sport_center.app import App, main

def mock_response_dict(status_code, data={}):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


def mock_response(status_code, data=[]):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_sign_in(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    mocked_print.assert_any_call('*** SIGN IN ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['1', 'userdosntexic', 'userdosntexic!'])
@patch('builtins.print')
def test_app_sign_in_nonexistent_user(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('>>>>>>>>>>>> SPORT ZONE <<<<<<<<<<<<')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_print.assert_any_call('This user does not exist!')


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['2', 'newUuser', 'sadasdsadsa@gmail.com','passwordPas89' ])
@patch('builtins.print')
def test_app_registration_existent_user(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('>>>>>>>>>>>> SPORT ZONE <<<<<<<<<<<<')
    mocked_print.assert_any_call('2:\tRegister')
    mocked_print.assert_any_call('This user already exists!')


@patch('requests.post', side_effect=[mock_response_dict(200)])
@patch('builtins.input', side_effect=['2', 'nuovousername', 'nuova@gmail.com', 'passwordd'])
@patch('builtins.print')
def test_app_registration_user(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('>>>>>>>>>>>> SPORT ZONE <<<<<<<<<<<<')
    mocked_print.assert_any_call('2:\tRegister')
    mocked_print.assert_any_call('Registration done!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'Key': '2aaec33e8100720d8281385d11503cc7631923cf'})])
@patch('builtins.input', side_effect=['1', 'username', 'Mimo01123'])
@patch('builtins.print')
def test_app_sign_in_with_correct_parameters(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_requests_post.assert_called()

    mocked_print.assert_any_call('>>>>>>>>>>>> SPORT ZONE <<<<<<<<<<<<')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_input.assert_called()
    mocked_print.assert_any_call('Login success')

