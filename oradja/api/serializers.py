from rest_framework import serializers

from oradja.db.docs.doc_processor import download_file_name
from oradja.models import UmvDocument


class UmvDocumentSerializer(serializers.ModelSerializer):
    download_file_name = serializers.SerializerMethodField()

    def get_download_file_name(self, obj):
        d_name = download_file_name({"umvdcm": obj.umvdcm, "file_name": obj.file_name})
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
