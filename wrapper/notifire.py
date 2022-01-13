from requests import Session
from typing import Dict, List
from enums import ApiPathEnum, ApiMethodEnum, ApiUrlEnum
from forms import EventPayloadForm, NotifireConfigForm, RequestForm, TriggerForm


class Notifire:
    def __init__(self, api_key: str, api_url: str = ApiUrlEnum.V1.value):
        self.session = Session()
        self.config = NotifireConfigForm(api_key=api_key, api_url=api_url)

    def _request(self, method: ApiMethodEnum, path: ApiPathEnum, params: Dict = None):

        form = RequestForm(method=method, path=path, params=params)

        url = self.config.api_url + form.path.value
        headers = {
            'Authorization': f'ApiKey {self.config.api_key}'
        }
        return self.session.request(form.method.value, url, headers=headers, params=form.params)

    def _post(self, path: ApiPathEnum, params: Dict = None):
        return self._request(ApiMethodEnum.POST, path, params=params)

    def trigger(self, event_name: str, user_id: str, first_name: str = None, last_name: str = None, email: str = None,
                channels: List[str] = None):
        event_payload = EventPayloadForm(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            channels=channels
        )
        form = TriggerForm(name=event_name, payload=event_payload)
        return self._post(ApiPathEnum.TRIGGER, params=form.dict(exclude_none=True))
