import email
from lib2to3.pgen2 import token
from urllib import request, response
import yaml
import base64
from time import sleep
from django.shortcuts import render
from rest_framework import generics
from .models import Job, User
from .serializers import JobSerializer, UserSerializer, ImageSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime


class ListJob(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class ListUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DetailJob(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LastestJob(generics.ListCreateAPIView):
    queryset = Job.objects.all().filter(
        job_status=0).order_by('-create_time')[:1]
    serializer_class = JobSerializer

# for doing register new user


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# for user login


class LoginView(APIView):
    def post(self, reqest):
        email = reqest.data['email']
        password = reqest.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("Email not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Password is not match!")

        payload = {
            'id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        respond = Response()
        # respond.set_cookie(key='jwt',value=token,httponly=True)
        respond.data = ({
            'jwt': token
        })

        return respond


class UserView(APIView):
    def post(self, request):
        # print(reqest.data['jwt'])
        token = request.data['jwt']

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(user_id=payload['id'])

        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request):
        token = request.data['jwt']
        first_name = request.data['first_name']
        last_name = request.data['last_name']

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(user_id=payload['id'])
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return Response({"status": "Changing complete !!!"})


class PasswordView(APIView):
    def put(self, request):
        token = request.data['jwt']
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(user_id=payload['id'])
        if not user.check_password(old_password):
            raise AuthenticationFailed("Password is not match!")
        else:
            user.set_password(new_password)
            user.save()
            return Response({"status": "Password is change!"})


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'msg': 'Logout Success'
        }
        return response


class ImageView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EditImageView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MakeDockerFile(APIView):
    def post(self,request):
        token = request.data['jwt']
        job_id = request.data['job_id']
        app_id = request.data['app_id']
        path = request.data['path']
        num_img = request.data['num_img']
        img_selected = request.data['img_selected']


        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(user_id=payload['id'])



        template = """apiVersion: batch/v1
kind: Job
metadata:
    name: """+job_id+"""
    namespace: jobdemonamespace
    labels:
        job_name: """+job_id+"""
spec:
    template:
        metadata:
            labels:
                app: my-job-pod-id
            name: my-job-pod-id
        spec:
            containers:
                - image: "shuffler:latest"
                imagePullPolicy: Never
                name: "shuffler"
                command:
                    - python3
                    - -u
                    - ./test.py """+user.user_id+""" """+job_id+""" """+app_id+""" """+path+""" """+img_selected+"""
                args:
                    - "Kubernetes"
            restartPolicy: Never"""
        with open('yaml_file/'+job_id+'.yaml', 'w') as yfile:
            yfile.write(template)

        job_data ={
            'job_id' : job_id,
            'user_id': user.user_id,
            'app_id' : app_id,
            'path' : path,
            'num_img' : num_img,
            'img_selected' : img_selected,
            'job_status' : "1"
        }
        
        serializer = JobSerializer(data=job_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "File is made!"})
