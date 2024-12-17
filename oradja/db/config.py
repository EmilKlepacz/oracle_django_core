import os

import oracledb

_OCI = "ORADJA_OCI"
_USER = "ORADJA_USER"
_PASSWORD = "ORADJA_PASSWORD"
_NAME = "ORADJA_NAME"
_HOST = "ORADJA_HOST"
_PORT = "ORADJA_PORT"


class MissingCredentialsError(Exception):
    pass


class MissingOracleInstantClient(Exception):
    pass


def init_oracle_client():
    instant_client_dir = os.environ.get(_OCI)

    if instant_client_dir is None or instant_client_dir == "":
        raise MissingOracleInstantClient(f"{_OCI} must be set")

    oracledb.init_oracle_client(lib_dir=instant_client_dir)


def get_credentials():
    user = os.environ.get(_USER)
    password = os.environ.get(_PASSWORD)
    name = os.environ.get(_NAME)
    host = os.environ.get(_HOST)
    port = os.environ.get(_PORT)

    if user is None or user == "":
        raise MissingCredentialsError(f"{_USER} must be set")

    if password is None or password == "":
        raise MissingCredentialsError(f"{_PASSWORD} must be set")

    if name is None or name == "":
        raise MissingCredentialsError(f"{_NAME} must be set")

    if host is None or host == "":
        raise MissingCredentialsError(f"{_HOST} must be set")

    if port is None or port == "":
        raise MissingCredentialsError(f"{_PORT} must be set")

    return {
        "user": user,
        "password": password,
        "name": name,
        "host": host,
        "port": port
    }
