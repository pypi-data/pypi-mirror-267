from enum import Enum


class UserAccountStatusEnum(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


class AuthenticationTypeEnum(Enum):
    USERNAME = "USERNAME"


class UserLogEventEnum(Enum):
    CREATED = "CREATED"
    DELETED = "DELETED"
