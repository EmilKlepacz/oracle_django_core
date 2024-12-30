from rest_framework import serializers

from oradja.db.docs.doc_processor import download_file_name
from oradja.models import UmvDocument, ApiUser


class ApiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUser
        fields = ["apiusr", "name"]


class UmvDocumentSerializer(serializers.ModelSerializer):
    download_file_name = serializers.SerializerMethodField()
    apiusr = ApiUserSerializer(read_only=True)

    def get_download_file_name(self, obj):
        d_name = download_file_name(obj)
        return d_name

    class Meta:
        model = UmvDocument
        # file_data missing
        fields = ["umvdcm",
                  "file_name",
                  "download_file_name",
                  "created_dati",
                  "updated_dati",
                  "internal",
                  "apiusr"]
