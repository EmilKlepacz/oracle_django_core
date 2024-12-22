from unittest import mock

import pytest

from oradja.db.config import get_credentials, MissingCredentialsError, init_oracle_client, MissingOracleInstantClient


@pytest.fixture
def mock_oracle_db_init_oracle_client():
    with mock.patch("oracledb.init_oracle_client") as mock_oracle_db_init_oracle_client:
        yield mock_oracle_db_init_oracle_client


def test_get_credentials_success(monkeypatch):
    monkeypatch.setenv("ORADJA_USER", "test_user")
    monkeypatch.setenv("ORADJA_PASSWORD", "test_password")
    monkeypatch.setenv("ORADJA_NAME", "test_name")
    monkeypatch.setenv("ORADJA_HOST", "test_host")
    monkeypatch.setenv("ORADJA_PORT", "test_port")

    credentials = get_credentials()

    assert credentials == {
        "user": "test_user",
        "password": "test_password",
        "name": "test_name",
        "host": "test_host",
        "port": "test_port",
    }


def test_get_credentials_missing_user(monkeypatch):
    monkeypatch.setenv("ORADJA_USER", "")
    monkeypatch.setenv("ORADJA_PASSWORD", "test_password")
    monkeypatch.setenv("ORADJA_NAME", "test_name")
    monkeypatch.setenv("ORADJA_HOST", "test_host")
    monkeypatch.setenv("ORADJA_PORT", "test_port")

    with pytest.raises(MissingCredentialsError, match="ORADJA_USER must be set"):
        get_credentials()


def test_get_credentials_missing_password(monkeypatch):
    monkeypatch.setenv("ORADJA_USER", "test_user")
    monkeypatch.setenv("ORADJA_PASSWORD", "")
    monkeypatch.setenv("ORADJA_NAME", "test_name")
    monkeypatch.setenv("ORADJA_HOST", "test_host")
    monkeypatch.setenv("ORADJA_PORT", "test_port")

    with pytest.raises(MissingCredentialsError, match="ORADJA_PASSWORD must be set"):
        get_credentials()


def test_get_credentials_missing_name(monkeypatch):
    monkeypatch.setenv("ORADJA_USER", "test_user")
    monkeypatch.setenv("ORADJA_PASSWORD", "test_password")
    monkeypatch.setenv("ORADJA_NAME", "")
    monkeypatch.setenv("ORADJA_HOST", "test_host")
    monkeypatch.setenv("ORADJA_PORT", "test_port")

    with pytest.raises(MissingCredentialsError, match="ORADJA_NAME must be set"):
        get_credentials()


def test_get_credentials_missing_host(monkeypatch):
    monkeypatch.setenv("ORADJA_USER", "test_user")
    monkeypatch.setenv("ORADJA_PASSWORD", "test_password")
    monkeypatch.setenv("ORADJA_NAME", "test_name")
    monkeypatch.setenv("ORADJA_HOST", "")
    monkeypatch.setenv("ORADJA_PORT", "test_port")

    with pytest.raises(MissingCredentialsError, match="ORADJA_HOST must be set"):
        get_credentials()


def test_get_credentials_missing_port(monkeypatch):
    monkeypatch.setenv("ORADJA_USER", "test_user")
    monkeypatch.setenv("ORADJA_PASSWORD", "test_password")
    monkeypatch.setenv("ORADJA_NAME", "test_name")
    monkeypatch.setenv("ORADJA_HOST", "test_host")
    monkeypatch.setenv("ORADJA_PORT", "")

    with pytest.raises(MissingCredentialsError, match="ORADJA_PORT must be set"):
        get_credentials()


def test_init_oracle_client_success(monkeypatch, mock_oracle_db_init_oracle_client):
    monkeypatch.setenv("ORADJA_OCI", "/test/path/oci")

    init_oracle_client()

    mock_oracle_db_init_oracle_client.assert_called_once_with(lib_dir="/test/path/oci")


def test_init_oracle_client_missing_oci(monkeypatch, mock_oracle_db_init_oracle_client):
    monkeypatch.setenv("ORADJA_OCI", "")

    with pytest.raises(MissingOracleInstantClient, match="ORADJA_OCI must be set"):
        init_oracle_client()

    mock_oracle_db_init_oracle_client.assert_not_called()
