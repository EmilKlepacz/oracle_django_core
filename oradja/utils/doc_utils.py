from oradja.models import UmvDocument


def list_docs(limit):
    docs = UmvDocument.objects.all()[:limit]
    for doc in docs:
        print(doc.file_name)
