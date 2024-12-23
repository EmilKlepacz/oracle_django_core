from datetime import date, timedelta

import pytest

from oradja.models import UmvDocument, ApiUser


@pytest.fixture
def umv_document_query_docs_limit_three():
    limit = 3
    yield limit, UmvDocument.query_docs(limit)


@pytest.fixture
def umv_document_query_docs_limit_three_with_blob():
    limit = 3
    yield limit, UmvDocument.query_docs(limit, fetch_file_blob=True)


@pytest.mark.django_db
def test_query_docs_with_default_limit_gives_correct_number_of_documents():
    default_limit = 100
    latest_documents = UmvDocument.query_docs()
    assert len(
        latest_documents) <= default_limit, f"Expected default limit of docs: {default_limit}, got {len(latest_documents)}"


@pytest.mark.django_db
def test_query_docs_returns_correct_number_of_documents(umv_document_query_docs_limit_three):
    limit, latest_documents = umv_document_query_docs_limit_three
    # Verify the length of the returned queryset
    assert len(latest_documents) <= limit, f"Expected at most {limit} documents, got {len(latest_documents)}."


@pytest.mark.django_db
def test_query_docs_returns_correct_documents_in_desc_order(umv_document_query_docs_limit_three):
    limit, latest_documents = umv_document_query_docs_limit_three

    # Verify that the results are ordered by "created_dati" descending
    created_dates = [doc["created_dati"] for doc in latest_documents]
    assert created_dates == sorted(created_dates,
                                   reverse=True), "Documents are not ordered by 'created_dati' descending."


@pytest.mark.django_db
def test_query_docs_returns_docs_with_required_columns(umv_document_query_docs_limit_three):
    _, latest_documents = umv_document_query_docs_limit_three

    required_columns = ["umvdcm", "file_name", "created_dati"]

    for doc in latest_documents:
        for column in required_columns:
            assert column in doc, f"Column {column} missing in document"


@pytest.mark.django_db
def test_query_docs_with_default_limit_with_blob_gives_correct_number_of_documents(
        umv_document_query_docs_limit_three_with_blob):
    _, latest_documents = umv_document_query_docs_limit_three_with_blob

    required_columns = ["umvdcm", "file_name", "created_dati", "file_data"]

    for doc in latest_documents:
        for column in required_columns:
            assert column in doc, f"Column {column} missing in document"


@pytest.mark.django_db
def test_query_docs_returns_docs_in_correct_date_range_from_date_present():
    today_minus_six_months = date.today() - timedelta(days=180)

    docs = UmvDocument.query_docs(created_dati_from=today_minus_six_months)

    # Access the first document
    assert docs.first().get("created_dati") >= today_minus_six_months


@pytest.mark.django_db
def test_query_docs_returns_docs_in_correct_date_range_to_date_present():
    today_minus_one_month = date.today() - timedelta(days=30)

    docs = UmvDocument.query_docs(created_dati_to=today_minus_one_month)

    # Access the last document in the queryset explicitly
    assert docs[len(docs) - 1]["created_dati"] <= today_minus_one_month


@pytest.mark.django_db
def test_query_docs_returns_docs_in_correct_date_range_from_to_date_present():
    today_minus_six_months = date.today() - timedelta(days=180)
    today_minus_one_month = date.today() - timedelta(days=30)

    docs = UmvDocument.query_docs(created_dati_from=today_minus_six_months, created_dati_to=today_minus_one_month)

    assert docs.first().get("created_dati") >= today_minus_six_months
    assert docs[len(docs) - 1]["created_dati"] <= today_minus_one_month


@pytest.mark.django_db
def test_query_docs_returns_correct_docs_by_ids():
    api_user = ApiUser.objects.get(name="api")

    doc1 = UmvDocument.objects.create(
        file_name="test1",
        file_data=b"Simple binary data",
        created_dati=date.today(),
        internal=False,
        notes="This is a test document.",
        apiusr=api_user,
    )
    doc1.save()

    doc2 = UmvDocument.objects.create(
        file_name="test2",
        file_data=b"Simple binary data",
        created_dati=date.today(),
        internal=False,
        notes="This is a test document.",
        apiusr=api_user,
    )
    doc2.save()

    doc3 = UmvDocument.objects.create(
        file_name="test1",
        file_data=b"Simple binary data",
        created_dati=date.today(),
        internal=False,
        notes="This is a test document.",
        apiusr=api_user,
    )
    doc3.save()

    results = UmvDocument.query_docs(ids=[doc1.umvdcm, doc2.umvdcm, doc3.umvdcm])
    results_list = list(results)

    # Assert that each document exists in the results
    assert any(result["umvdcm"] == doc1.umvdcm for result in results_list), f"Document {doc1.umvdcm} not found in results"
    assert any(result["umvdcm"] == doc2.umvdcm for result in results_list), f"Document {doc2.umvdcm} not found in results"
    assert any(result["umvdcm"] == doc3.umvdcm for result in results_list), f"Document {doc3.umvdcm} not found in results"
