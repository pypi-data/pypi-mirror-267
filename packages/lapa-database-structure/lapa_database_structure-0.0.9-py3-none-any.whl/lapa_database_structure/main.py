from enum import Enum


class DatabasesEnum(str, Enum):
    lapa = "lapa"
    lapa_testing = "lapa_testing"


class SchemaEnum(str, Enum):
    public = "public"
    file_storage = "file_storage"
    authentication = "authentication"


class TablesEnum(str, Enum):
    file = "file"

    user = "user"
    authentication_username = "authentication_username"
    user_profile = "user_profile"
    user_authentication = "user_authentication"
    user_log = "user_log"
