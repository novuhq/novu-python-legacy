import pytest
import requests
from unittest import mock
from enums import ApiMethodEnum, ApiPathEnum, ApiUrlEnum
from wrapper.notifire import Notifire


def test_valid_notifire_config(api_config):
    notifire_client = Notifire(**api_config)
    for key in api_config:
        assert notifire_client.config.dict().get(key) == api_config.get(key)


def test_missing_api_url_gets_default_url():
    notifire_client = Notifire('only-passed-key')
    assert notifire_client.config.api_url == ApiUrlEnum.V1.value


@pytest.mark.parametrize('method, path', [
    (ApiPathEnum.TRIGGER, ApiPathEnum.TRIGGER),
    (ApiMethodEnum.POST, ApiMethodEnum.POST)
])
def test_wrong_request_method_or_path_raises_value_error(api_config, method, path):
    with mock.patch.object(requests.Session, 'request') as request, \
         pytest.raises(ValueError):
        notifire_client = Notifire(**api_config)
        notifire_client._request(method, path)
        request.assert_not_called()


def test_null_params_gets_empty_dict(api_config):
    with mock.patch.object(requests.Session, 'request') as request:
        method = ApiMethodEnum.POST
        path = ApiPathEnum.TRIGGER
        notifire_client = Notifire(**api_config)
        notifire_client._request(method, path)

        expected_method = method.value
        expected_params = {}
        expected_url = api_config.get('api_url') + path.value
        expected_headers = {
            'Authorization': f'ApiKey {api_config.get("api_key")}'
        }
        request.assert_called_once_with(expected_method, expected_url, headers=expected_headers, params=expected_params)


def test_notifire_request_calls_requests_request_correctly(api_config):
    with mock.patch.object(requests.Session, 'request') as request:
        method = ApiMethodEnum.POST
        path = ApiPathEnum.TRIGGER
        params = {
            'name': 'testing name',
            'payload': {
                'user_id': 1,
                'email': 'user@fakeemail.com'
            }
        }
        notifire_client = Notifire(**api_config)
        notifire_client._request(method, path, params=params)

        expected_method = method.value
        expected_params = params
        expected_url = api_config.get('api_url') + path.value
        expected_headers = {
            'Authorization': f'ApiKey {api_config.get("api_key")}'
        }
        request.assert_called_once_with(expected_method, expected_url, headers=expected_headers, params=expected_params)


def test_notifire_post_calls_notifire_request_correctly(api_config):
    with mock.patch.object(Notifire, '_request') as _request:
        path = ApiPathEnum.TRIGGER
        params = {
            'name': 'testing name',
            'payload': {
                'user_id': 1,
                'email': 'user@fakeemail.com'
            }
        }
        notifire_client = Notifire(**api_config)
        notifire_client._post(path, params=params)

        expected_method = ApiMethodEnum.POST
        expected_path = path
        expected_params = params
        _request.assert_called_once_with(expected_method, expected_path, params=expected_params)
