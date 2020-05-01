import os
import pytest
from mock import MagicMock, Mock, call, mock_open, patch

from rpgetter.utils import google


class TestGoogleAuthenticator(object):

    def test_init_value_error(self):
        with pytest.raises(ValueError):
            google.GoogleAuthenticator(None, None)

    @patch('pickle.load')
    def test_get_credentials_by_pickle_valid(self, mock_pickle_load):
        mock_pickle_load.return_value = MagicMock(valid=True)
        credentials = google.GoogleAuthenticator._get_credentials_by_pickle(MagicMock())
        assert credentials.valid

    @patch('google.auth.transport.requests.Request')
    @patch('pickle.load')
    def test_get_credentials_by_pickle_invalid(self, mock_pickle_load, mock_request):
        invalid_mock_credentials = MagicMock(valid=False, expired=True, refresh_token=True)
        invalid_mock_credentials.refresh.return_value = MagicMock(valid=True)
        mock_pickle_load.return_value = invalid_mock_credentials
        credentials = google.GoogleAuthenticator._get_credentials_by_pickle(MagicMock())
        assert credentials.valid

    @patch.object(google.GoogleAuthenticator, '_get_credentials_by_json')
    @patch.object(google.GoogleAuthenticator, '_get_credentials_by_pickle')
    def test_get_credentials_credentials(self, mock_pickle_credentials, mock_pickle_json):
        mock_pickle_credentials.return_value = 'True'
        mock_pickle_json.return_value = 'False'
        authenticator = google.GoogleAuthenticator(credentials_json=None, token_pickle='token.pickle')

        assert authenticator.credentials
        mock_pickle_credentials.assert_called_once()
        mock_pickle_json.assert_not_called()

    @patch.object(google.GoogleAuthenticator, '_get_credentials_by_json')
    @patch.object(google.GoogleAuthenticator, '_get_credentials_by_pickle')
    def test_get_credentials_json(self, mock_pickle_credentials, mock_pickle_json):
        mock_pickle_credentials.return_value = 'False'
        mock_pickle_json.return_value = 'True'
        authenticator = google.GoogleAuthenticator(credentials_json='credentials.json', token_pickle=None)

        assert authenticator.credentials
        mock_pickle_credentials.assert_not_called()
        mock_pickle_json.assert_called_once()

    @patch.object(google.GoogleAuthenticator, '_get_credentials_by_json')
    @patch.object(google.GoogleAuthenticator, '_get_credentials_by_pickle')
    def test_get_credentials_both(self, mock_pickle_credentials, mock_pickle_json):
        mock_pickle_credentials.return_value = 'True'
        mock_pickle_json.return_value = 'False'
        authenticator = google.GoogleAuthenticator(credentials_json='credentials.json', token_pickle='token.pickle')

        assert authenticator.credentials
        mock_pickle_credentials.assert_called_once()
        mock_pickle_json.assert_not_called()

    @patch.object(google.GoogleAuthenticator, '_get_credentials_by_json')
    @patch.object(google.GoogleAuthenticator, '_get_credentials_by_pickle')
    def test_save(self, mock_pickle_credentials, mock_pickle_json, tmpdir):
        mock_pickle_credentials.return_value = 'True'
        mock_pickle_json.return_value = 'True'
        authenticator = google.GoogleAuthenticator(credentials_json='credentials.json', token_pickle='token.pickle')

        file_path = os.path.join(tmpdir, 'token.pickle')
        authenticator.save(file_path)

        assert os.path.exists(file_path)
