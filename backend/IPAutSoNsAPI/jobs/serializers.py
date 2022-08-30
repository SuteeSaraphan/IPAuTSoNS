from rest_framework import serializers
from .models import Job
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'job_id',
            'user_id',
            'path',
            'num_img',
            'persent',
            'job_status'
        )
        model = Job