from datetime import date
from typing import List, Optional

from rest_framework import generics

from oradja.api.pagination import StandardPagination
from oradja.api.parsers.req_params_parser import RequestParamsParser
from oradja.api.serializers import UmvDocumentSerializer
from oradja.file_manager.file_type import FileType
from oradja.models import UmvDocument


class UmvDocumentListView(generics.ListAPIView):
    queryset = UmvDocument.objects.all()
    serializer_class = UmvDocumentSerializer
    pagination_class = StandardPagination


class UmvDocumentDetailView(generics.RetrieveAPIView):
    queryset = UmvDocument.objects.all()
    serializer_class = UmvDocumentSerializer


class UmvDocumentSearchView(generics.ListAPIView):
    serializer_class = UmvDocumentSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        """
        Filters the queryset based on parameters passed in the URL.
        """
        created_dati_from = RequestParamsParser.parse(val=self.request.query_params.get("created_dati_from", None),
                                                      type_=date)

        created_dati_to = RequestParamsParser.parse(val=self.request.query_params.get("created_dati_to", None),
                                                    type_=date)

        limit = RequestParamsParser.parse(val=self.request.query_params.get("limit", None),
                                          type_=int)

        ids = RequestParamsParser.parse(val=self.request.query_params.get("ids", None),
                                        type_=list,
                                        list_type=int)

        file_types_str: Optional[List[str]] = RequestParamsParser.parse(
            val=self.request.query_params.get("file_types", None),
            type_=list,
            list_type=str)

        file_types: Optional[List[FileType]] = [FileType.get_by_value(file_type) for file_type in
                                                file_types_str] if file_types_str else None

        queryset = UmvDocument.search_docs(limit=limit,
                                           created_dati_from=created_dati_from,
                                           created_dati_to=created_dati_to,
                                           ids=ids,
                                           file_types=file_types)

        return queryset
