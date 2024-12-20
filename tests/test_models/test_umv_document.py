# todo : test with mock to not work with real db
from datetime import date, timedelta

import pytest
from oradja.models import UmvDocument


@pytest.fixture
def umv_document_get_latest_limit_three():
    limit = 3
    yield limit, UmvDocument.get_latest(limit)


@pytest.mark.django_db
def test_get_latest_with_default_limit_gives_correct_number_of_documents():
    default_limit = 100
    latest_documents = UmvDocument.get_latest()
    assert len(
        latest_documents) <= default_limit, f"Expected default limit of docs: {default_limit}, got {len(latest_documents)}"


@pytest.mark.django_db
def test_get_latest_returns_correct_number_of_documents(umv_document_get_latest_limit_three):
    limit, latest_documents = umv_document_get_latest_limit_three
    # Verify the length of the returned queryset
    assert len(latest_documents) <= limit, f"Expected at most {limit} documents, got {len(latest_documents)}."


@pytest.mark.django_db
def test_get_latest_returns_correct_documents_in_desc_order(umv_document_get_latest_limit_three):
    limit, latest_documents = umv_document_get_latest_limit_three

    # Verify that the results are ordered by "created_dati" descending
    created_dates = [doc["created_dati"] for doc in latest_documents]
    assert created_dates == sorted(created_dates,
                                   reverse=True), "Documents are not ordered by 'created_dati' descending."


@pytest.mark.django_db
def test_get_latest_returns_docs_with_required_columns(umv_document_get_latest_limit_three):
    _, latest_documents = umv_document_get_latest_limit_three

    required_columns = ["umvdcm", "file_name", "created_dati"]

    for doc in latest_documents:
        for column in required_columns:
            assert column in doc, f"Column {column} missing in document"


@pytest.mark.django_db
def test_get_latest_returns_docs_in_correct_date_range_from_date_present():
    today_minus_six_months = date.today() - timedelta(days=180)

    docs = UmvDocument.get_latest(created_dati_from=today_minus_six_months)

    # Access the first document
    assert docs.first().get("created_dati") >= today_minus_six_months


@pytest.mark.django_db
def test_get_latest_returns_docs_in_correct_date_range_to_date_present():
    today_minus_one_month = date.today() - timedelta(days=30)

    docs = UmvDocument.get_latest(created_dati_to=today_minus_one_month)

    # Access the last document in the queryset explicitly
    assert docs[len(docs) - 1]["created_dati"] <= today_minus_one_month


@pytest.mark.django_db
def test_get_latest_returns_docs_in_correct_date_range_from_to_date_present():
    today_minus_six_months = date.today() - timedelta(days=180)
    today_minus_one_month = date.today() - timedelta(days=30)

    docs = UmvDocument.get_latest(created_dati_from=today_minus_six_months, created_dati_to=today_minus_one_month)

    assert docs.first().get("created_dati") >= today_minus_six_months
    assert docs[len(docs) - 1]["created_dati"] <= today_minus_one_month
