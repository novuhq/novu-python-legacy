from typing import Optional, List, Dict
from pydantic import BaseModel, validator, Extra
from enums import ChannelTypeEnum, ApiMethodEnum, ApiPathEnum


class RequestForm(BaseModel):
    method: ApiMethodEnum
    path: ApiPathEnum
    params: Optional[Dict]

    @validator('params')
    def null_params_means_empty_dict(cls, v):
        if v is None:
            return {}
        return v


class NotifireConfigForm(BaseModel):
    api_url: str
    api_key: str


class EventPayloadForm(BaseModel):

    class Config:
        extra = Extra.allow.value

    user_id: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    channels: Optional[List[str]]

    @validator('channels')
    def all_channels_must_be_in_channel_type_enum(cls, v):
        if v is not None:
            possible_channels = ChannelTypeEnum.values_set()
            for channel in v:
                if channel not in possible_channels:
                    raise ValueError(f'Channel {channel} not in supported channel types. Options are {", ".join(possible_channels)}')
        return v


class TriggerForm(BaseModel):
    name: str
    payload: EventPayloadForm
