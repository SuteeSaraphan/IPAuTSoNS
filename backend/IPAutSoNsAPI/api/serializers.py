from rest_framework import serializers
from .models import Job, User


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'job_id',
            'user_id',
            'app_id',
            'path',
            'num_img',
            'img_selected',
            'persent',
            'job_status',
            'create_time'
        )
        model = Job


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user_id',
            'password',
            'email',
            'is_vip'
        )
        model = User
