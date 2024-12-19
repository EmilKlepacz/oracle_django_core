# todo : test with mock to not work with real db
import pytest
from oradja.models import UmvDocument


@pytest.fixture
def umv_document_get_latest():
    limit = 3
    yield limit, UmvDocument.get_latest(limit)


@pytest.mark.django_db
def test_get_latest_returns_correct_number_of_documents(umv_document_get_latest):
    limit, latest_documents = umv_document_get_latest
    # Verify the length of the returned queryset
    assert len(latest_documents) <= limit, f"Expected at most {limit} documents, got {len(latest_documents)}."


@pytest.mark.django_db
def test_get_latest_returns_correct_documents_in_desc_order(umv_document_get_latest):
    limit, latest_documents = umv_document_get_latest

    # Verify that the results are ordered by "created_dati" descending
    created_dates = [doc["created_dati"] for doc in latest_documents]
    assert created_dates == sorted(created_dates,
                                   reverse=True), "Documents are not ordered by 'created_dati' descending."


@pytest.mark.django_db
def test_get_latest_returns_docs_with_required_columns(umv_document_get_latest):
    _, latest_documents = umv_document_get_latest

    required_columns = ["umvdcm", "file_name", "created_dati"]

    for doc in latest_documents:
        for column in required_columns:
            assert column in doc, f"Column {column} missing in document"
