from enum import Enum, unique


# Custom Enum class of unique values with useful method of returning a values set

@unique
class CustomEnum(Enum):
    @classmethod
    def values_set(cls):
        return set([name.value for name in list(cls)])


# Api related enums

class ApiUrlEnum(CustomEnum):
    V1 = 'https://api.notifire.co/v1'


class ApiPathEnum(CustomEnum):
    TRIGGER = '/events/trigger'


class ApiMethodEnum(CustomEnum):
    POST = 'POST'


# Channel related enums

class ChannelTypeEnum(CustomEnum):
    IN_APP = 'in_app'
    EMAIL = 'email'
    SMS = 'sms'
