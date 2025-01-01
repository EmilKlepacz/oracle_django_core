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


class UmvDocumentSearchSerializer(serializers.Serializer):
    created_dati_from = serializers.DateField(required=True, help_text="The start date for filtering documents.")
    created_dati_to = serializers.DateField(required=True, help_text="The end date for filtering documents.")
    limit = serializers.IntegerField(required=False, min_value=1,
                                     help_text="The maximum number of documents to retrieve.")

    file_types = serializers.ListField(
        child=serializers.CharField(max_length=10),
        required=False,
        help_text="A list of file types to filter documents (e.g., pdf, txt)."
    )

    def create(self, validated_data):
        """Dummy create method to satisfy DRF requirements."""
        return validated_data

    def update(self, instance, validated_data):
        """Dummy update method to satisfy DRF requirements."""
        return validated_data

from rest_framework import serializers

class UmvDocumentOutputSerializer(serializers.Serializer):
    umvdcm = serializers.IntegerField()
    file_name = serializers.CharField(max_length=255)
    apiusr = ApiUserSerializer(read_only=True)
    created_dati = serializers.DateField(required=True)
    updated_dati = serializers.DateField(required=True)
