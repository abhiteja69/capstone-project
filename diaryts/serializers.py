from rest_framework import serializers
from . models import Diaryt


class DiarytSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diaryt
        fields = ('created_by', 'title', 'emotion', 'description', 'created_at')


