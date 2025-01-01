import logging
from datetime import date
from typing import Optional, List

from django.core.exceptions import ValidationError
from rest_framework import generics

from oradja.api.pagination import StandardPagination
from oradja.api.parsers.req_params_parser import RequestParamsParser
from oradja.api.serializers import UmvDocumentSearchSerializer, UmvDocumentSerializer, UmvDocumentOutputSerializer
from oradja.file_manager.file_type import FileType
from oradja.models import UmvDocument
from rest_framework.response import Response
from rest_framework import status


class UmvDocumentListView(generics.ListAPIView):
    queryset = UmvDocument.objects.all()
    serializer_class = UmvDocumentSerializer
    pagination_class = StandardPagination


class UmvDocumentDetailView(generics.RetrieveAPIView):
    queryset = UmvDocument.objects.all()
    serializer_class = UmvDocumentSerializer


class UmvDocumentSearchUrlView(generics.ListAPIView):
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


class UmvDocumentSearchView(generics.CreateAPIView):
    serializer_class = UmvDocumentSearchSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        """
        Filters the queryset based on parameters passed in the request body (JSON payload).
        """
        # Ensure the request content type is application/json
        if self.request.content_type != 'application/json':
            raise ValidationError("Payload must be application/json type")

        # Extract validated data from the serializer
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Retrieve values from the validated serializer data
        created_dati_from = validated_data.get("created_dati_from")
        created_dati_to = validated_data.get("created_dati_to")
        limit = validated_data.get("limit", 3)  # Default limit to 3 if not provided
        file_types = [FileType.get_by_value(file_type) for file_type in validated_data.get("file_types")]

        # Perform the search operation using extracted parameters
        queryset = UmvDocument.search_docs(
            limit=limit,
            created_dati_from=created_dati_from,
            created_dati_to=created_dati_to,
            file_types=file_types
        )
        return queryset

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to return filtered results.
        """
        # Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(self.get_queryset(), request)

        if page is not None:
            output_serializer = UmvDocumentOutputSerializer(page, many=True)
            return paginator.get_paginated_response(output_serializer.data)

        # If no pagination applied, return full response
        output_serializer = UmvDocumentOutputSerializer(self.get_queryset(), many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
