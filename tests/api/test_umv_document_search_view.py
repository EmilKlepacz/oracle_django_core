import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def endpoint_url():
    return "/api/umvdocuments/search/"


@pytest.mark.django_db
def test_valid_payload(api_client, endpoint_url):
    payload = {
        "created_dati_from": "2023-01-01",
        "created_dati_to": "2024-01-01",
        "limit": 10,
        "file_types": ["pdf", "jpg"]
    }

    response = api_client.post(endpoint_url, data=payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data, "Response data is not paginated"
    assert len(response.data["results"]) <= 10, f"Response has to many results"


@pytest.mark.django_db
def test_missing_required_field(api_client, endpoint_url):
    payload = {
        # Missing created_dati_from
        "created_dati_to": "2024-01-01",
        "limit": 5,
        "file_types": ["pdf"]
    }
    response = api_client.post(endpoint_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "created_dati_from" in response.data


@pytest.mark.django_db
def test_invalid_data_type(api_client, endpoint_url):
    payload = {
        "created_dati_from": "2023-01-01",
        "created_dati_to": "2024-01-01",
        "limit": "three",  # Invalid data type for limit
        "file_types": ["pdf"]
    }
    response = api_client.post(endpoint_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "limit" in response.data


@pytest.mark.django_db
def test_empty_payload(api_client, endpoint_url):
    payload = {}  # No data provided
    response = api_client.post(endpoint_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_date_range_validation(api_client, endpoint_url):
    payload = {
        "created_dati_from": "2024-01-01",
        "created_dati_to": "2023-01-01",  # Invalid range
        "limit": 10,
        "file_types": ["pdf"]
    }
    response = api_client.post(endpoint_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response.data


@pytest.mark.django_db
def test_limit_validation(api_client, endpoint_url):
    payload = {
        "created_dati_from": "2023-01-01",
        "created_dati_to": "2024-01-01",
        "limit": -10,  # Invalid limit
        "file_types": ["pdf"]
    }
    response = api_client.post(endpoint_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "limit" in response.data


@pytest.mark.django_db
def test_file_types_validation(api_client, endpoint_url):
    payload = {
        "created_dati_from": "2023-01-01",
        "created_dati_to": "2024-01-01",
        "limit": 10,  # Invalid limit
        "file_types": ["exe"]
    }
    response = api_client.post(endpoint_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response.data


import pytest
from rest_framework import status


@pytest.mark.django_db
def test_payload_with_wrong_content_type(api_client, endpoint_url):
    xml_payload = """
    <request>
        <created_dati_from>2023-01-01</created_dati_from>
        <created_dati_to>2024-01-01</created_dati_to>
        <limit>10</limit>
        <file_types>
            <type>pdf</type>
        </file_types>
    </request>
    """

    with pytest.raises(ValidationError, match="Payload must be application/json type"):
        response = api_client.post(
            endpoint_url,
            data=xml_payload,  # Use 'data' for raw XML payloads
            content_type="application/xml"  # Set the Content-Type header to XML
        )
