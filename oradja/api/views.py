from rest_framework import generics

from oradja.api.pagination import StandardPagination
from oradja.api.serializers import UmvDocumentSerializer
from oradja.models import UmvDocument


class UmvDocumentListView(generics.ListAPIView):
    # todo: remove slicing when pagination will be done
    queryset = UmvDocument.objects.all()
    serializer_class = UmvDocumentSerializer
    pagination_class = StandardPagination


class UmvDocumentDetailView(generics.RetrieveAPIView):
    queryset = UmvDocument.objects.all()
    serializer_class = UmvDocumentSerializer
