from ctypes import sizeof
from lib2to3.pgen2 import token
from msilib.schema import Error
from operator import length_hint
import random
import string
from time import sleep
from django.shortcuts import render
from requests import delete
from rest_framework import generics
from .models import Folder_img, Image, Job, User
from .serializers import JobSerializer, UserSerializer, ImageSerializer, FolderImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import base64
from pathlib import Path


# for Authentication user with JWT


def Authentication(token):
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')

    return payload


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
    # for get user data
    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        user = User.objects.get(user_id=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # for change user data
    def put(self, request):
        token = request.data['jwt']
        first_name = request.data['first_name']
        last_name = request.data['last_name']

        payload = Authentication(token)

        user = User.objects.get(user_id=payload['id'])
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return Response({"status": "Changing complete !!!"})


class PasswordView(APIView):
    # for change user password
    def put(self, request):
        token = request.data['jwt']
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        payload = Authentication(token)

        user = User.objects.get(user_id=payload['id'])
        if not user.check_password(old_password):
            raise AuthenticationFailed("Password is not match!")
        else:
            user.set_password(new_password)
            user.save()
            return Response({"status": "Password is change!"})


class ImageView(APIView):

    #get image
    def get(self, request, folder_id):
        temp_respond = []
        token = request.META['HTTP_JWT']
        payload = Authentication(token)

        folder_serializer = FolderImageSerializer(
            Folder_img.objects.get(folder_id=folder_id)
        )

        img_serializer = ImageSerializer(
            Image.objects.all().filter(user_id=payload['id'], img_folder=folder_serializer.data['folder_name']), many=True)
        for i in img_serializer.data:
            try:
                with open('C:/IPAuTSoNS/backend/IPAutSoNsAPI'+os.path.join(i['path']),'rb') as image_file:
                    image_data = base64.b64encode(image_file.read())
                    temp_img_data ={
                        'img_id':i['img_id'],
                        'user_id':i['user_id'],
                        'img_type':i['img_type'],
                        'img_folder':i['img_folder'],
                        'path':i['path'],
                        'img_size':i['img_size'],
                        'img_data' : image_data
                    }
                    temp_respond.append(temp_img_data)


            except BaseException as error:
                print(error)

        return Response(temp_respond)

    #add image
    def post(self, request):
        token = request.data['jwt']
        folder = request.data['folder']
        payload = Authentication(token)
        user = User.objects.get(user_id=payload['id'])

        for img_file in request.FILES.getlist('img_file'):
            # print("name : "+str(img_file.name))
            # print("size : "+str(img_file.size)+" byte")
            # print("type : " +img_file.content_type)
            print("------------------")
            img_data = {
                'img_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
                'user_id': user.user_id,
                'img_type': img_file.content_type,
                'img_folder': folder,
                'path': img_file,
                'img_size': img_file.size
            }
            serializer = ImageSerializer(data=img_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("file "+img_file.name+" upload done")

        return Response({"status": "Upload done!"})

    #delete image
    def delete(self, request, folder_id):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        img_id = folder_id
        image = Image.objects.get(img_id=img_id)
        try:
            os.remove('C:/IPAuTSoNS/backend/IPAutSoNsAPI/media/'+os.path.join(str(image.path)))
        except BaseException as error:
            print(error)
            return Response({"status": "Delete fail ! try again"})
        else:
            image.delete()
            image.save()
            return Response({"status": "Delete done!"})

        

        

class AllImageView(APIView):
    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        serializer = ImageSerializer(
            Image.objects.all().filter(user_id=payload['id']), many=True)
        return Response(serializer.data)


class FolderView(APIView):
    def post(self, request):
        token = request.data['jwt']
        payload = Authentication(token)
        folder_path = os.path.join(r'C:\IPAuTSoNS\backend\IPAutSoNsAPI\media',
                                   payload['id'], "root", request.data['folder_name'])
        try:
            os.mkdir(folder_path)
        except OSError as error:
            print(error)
            return Response({'status': '!!! Somthing is wrong try again !!!'})
        else:
            folder_data = {
                'folder_id': request.data['folder_id'],
                'user_id': payload['id'],
                'folder_name': request.data['folder_name'],
                'path': folder_path,
                'is_hidden': False
            }

            serializer = FolderImageSerializer(data=folder_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': '!!! Create new folder complete !!!'})

    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        serializer = FolderImageSerializer(
            Folder_img.objects.all().filter(user_id=payload['id']), many=True)
        return Response(serializer.data)


class MakeDockerFile(APIView):
    def post(self, request):
        token = request.data['jwt']
        job_id = request.data['job_id']
        app_id = request.data['app_id']
        path = request.data['path']
        num_img = request.data['num_img']
        img_selected = request.data['img_selected']

        payload = Authentication(token)

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

        job_data = {
            'job_id': job_id,
            'user_id': user.user_id,
            'app_id': app_id,
            'path': path,
            'num_img': num_img,
            'img_selected': img_selected,
            'job_status': "1"
        }

        serializer = JobSerializer(data=job_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "File is made!"})
