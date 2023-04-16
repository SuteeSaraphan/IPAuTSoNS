from rest_framework import serializers
from .models import *


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'job_id',
            'user_id',
            'product_id',
            'payment_id',
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
            'is_vip',
            'first_name',
            'last_name',
        )
        model = User

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'img_id',
            'user_id',
            'img_type',
            'path',
            'img_size',
            'img_folder'
        )
        model = Image_file


class FolderImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user_id',
            'folder_id',
            'folder_name',
            'path',
            'is_hidden'
        )
        model = Folder_img


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'product_id',
            'user_id',
            'product_name',
            'product_type',
            'model',
            'price',
            'path',
            'product_img',
            'last_update',
            'detail'
        )
        model = Product


class Login_logSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'login_log_id',
            'user_id',
            'login_time'
        )
        model = Login_log


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'payment_id',
            'user_id',
            'product_id',
            'type',
            'pay_time',
            'credit'

        )
        model = Payment
