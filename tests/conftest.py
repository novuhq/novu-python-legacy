import pytest


@pytest.fixture
def api_config():
    return {
        'api_key': 'this-is-not-a-real-key',
        'api_url': 'https://thisisnotarealurl.com/api/v1'
    }
