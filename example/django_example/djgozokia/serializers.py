from rest_framework import serializers

from django.contrib.auth import get_user_model

from scanners.models import Scanner


class ScannerListSerializer(serializers.Serializer):
    website = serializers.EmailField()
    type = serializers.CharField(max_length=100)

    class Meta:
        model = Scanner
        fields = ('id', 'website', 'type')
