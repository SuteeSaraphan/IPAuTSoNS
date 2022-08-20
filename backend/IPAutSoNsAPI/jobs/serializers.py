from rest_framework import serializers
from .models import Job
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'job_id',
            'description',
        )
        model = Job