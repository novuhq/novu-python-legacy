import pytest
import requests
from pydantic import ValidationError
from unittest import mock
from enums import ApiPathEnum, ApiMethodEnum
from wrapper.notifire import Notifire


def test_notifire_trigger_calls_notifire_post_correctly(api_config):
    with mock.patch.object(Notifire, '_post') as _post:
        event_name = 'testing name'
        user_id = '152'
        first_name = 'John'
        last_name = 'Doe'
        email = 'fake@email.com'

        notifire_client = Notifire(**api_config)
        notifire_client.trigger(event_name, user_id, first_name=first_name, last_name=last_name, email=email)

        expected_path = ApiPathEnum.TRIGGER
        expected_params = {
            'name': event_name,
            'payload': {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
        }
        _post.assert_called_once_with(expected_path, params=expected_params)


def test_notifire_trigger_calls_requests_request_correctly(api_config):
    with mock.patch.object(requests.Session, 'request') as request:
        event_name = 'testing name'
        user_id = '152'
        first_name = 'John'
        last_name = 'Doe'
        email = 'fake@email.com'

        notifire_client = Notifire(**api_config)
        notifire_client.trigger(event_name, user_id, first_name=first_name, last_name=last_name, email=email)

        expected_method = ApiMethodEnum.POST.value
        expected_url = api_config.get('api_url') + ApiPathEnum.TRIGGER.value
        expected_headers = {
            'Authorization': f'ApiKey {api_config.get("api_key")}'
        }
        expected_params = {
            'name': event_name,
            'payload': {
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
        }
        request.assert_called_once_with(expected_method, expected_url, headers=expected_headers, params=expected_params)


@pytest.mark.parametrize('event_name, user_id', [
    (None, '1234'),
    ('Some event', None),
    (None, None)
])
def test_trigger_requires_user_id_and_event_name_to_make_request(api_config, event_name, user_id):
    with mock.patch.object(requests.Session, 'request') as request, \
         pytest.raises(ValidationError):
        notifire_client = Notifire(**api_config)
        notifire_client.trigger(event_name, user_id)
        request.assert_not_called()


def test_every_channel_must_be_in_channel_type_enum(api_config):
    with mock.patch.object(requests.Session, 'request') as request, \
         pytest.raises(ValidationError):
        notifire_client = Notifire(**api_config)
        notifire_client.trigger('Some event', 'some_user_id', channels=['sms', 'email', 'smoke_signal'])
        request.assert_not_called()
