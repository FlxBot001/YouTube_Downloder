from rest_framework import serializers
from .models import Download

class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = ['id', 'url', 'format_id', 'title', 'file_size', 'status', 'download_url', 'created_at']
        read_only_fields = ['title', 'file_size', 'status', 'download_url', 'created_at']