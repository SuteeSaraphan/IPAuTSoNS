from ctypes import sizeof
from io import BytesIO, StringIO
from lib2to3.pgen2 import token
from operator import length_hint
import random
import shutil
import string
from time import sleep
from django.shortcuts import render
from requests import delete
from rest_framework import generics
from .models import Folder_img, Job, User, Image_file
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
from PIL import Image


# for Authentication user with JWT


def Authentication(token):
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'IPAutSoNs', algorithms=['HS256'])
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
        user = User.objects.get(email=email)

        if user is None:
            raise AuthenticationFailed("Email not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Password is not match!")

        payload = {
            'id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'IPAutSoNs', algorithm='HS256')

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

    # send image to web
    def get(self, request, type, folder_id):
        temp_respond = []
        token = request.META['HTTP_JWT']
        payload = Authentication(token)

        # send compact data of all image to web
        if (type == "all"):
            folder_serializer = FolderImageSerializer(
                Folder_img.objects.get(folder_id=folder_id)
            )

            img_serializer = ImageSerializer(
                Image_file.objects.all().filter(user_id=payload['id'], img_folder=folder_serializer.data['folder_name']), many=True)
            for i in img_serializer.data:
                file_type = (i['img_type'].split('/'))[1]
                try:
                    with Image.open('C:/IPAuTSoNS/backend/IPAutSoNsAPI'+str(i['path'])) as image_file_temp:
                        percentage = 0.1
                        width, height = image_file_temp.size
                        resized_dimensions = (
                            int(width * percentage), int(height * percentage))
                        resized_image = image_file_temp.resize(
                            resized_dimensions)
                        buffer = BytesIO()
                        resized_image.save(buffer, format=file_type)
                        image_data = base64.b64encode(buffer.getvalue())

                        temp_img_data = {
                            'img_id': i['img_id'],
                            'user_id': i['user_id'],
                            'img_type': i['img_type'],
                            'img_folder': i['img_folder'],
                            'path': i['path'],
                            'img_size': i['img_size'],
                            'img_data': image_data
                        }
                        temp_respond.append(temp_img_data)

                except BaseException as error:
                    print(error)

            return Response(temp_respond)

        # send full data of one image to web
        elif (type == 'once'):
            img_serializer = ImageSerializer(
                Image_file.objects.all().filter(img_id=folder_id), many=True)
            for i in img_serializer.data:
                file_type = (i['img_type'].split('/'))[1]
                try:
                    with Image.open('C:/IPAuTSoNS/backend/IPAutSoNsAPI'+str(i['path'])) as image_file_temp:
                        percentage = 1
                        width, height = image_file_temp.size
                        resized_dimensions = (
                            int(width * percentage), int(height * percentage))
                        resized_image = image_file_temp.resize(
                            resized_dimensions)
                        buffer = BytesIO()
                        resized_image.save(buffer, format=file_type)
                        image_data = base64.b64encode(buffer.getvalue())

                        temp_img_data = {
                            'img_id': i['img_id'],
                            'user_id': i['user_id'],
                            'img_type': i['img_type'],
                            'img_folder': i['img_folder'],
                            'path': i['path'],
                            'img_size': i['img_size'],
                            'img_data': image_data
                        }
                        temp_respond.append(temp_img_data)

                except BaseException as error:
                    print(error)

            return Response(temp_respond)

        # count image to create page list in web
        elif (type == 'count'):
            folder_serializer = FolderImageSerializer(
                Folder_img.objects.get(folder_id=folder_id)
            )

            img_serializer = ImageSerializer(
                Image_file.objects.all().filter(user_id=payload['id'], img_folder=folder_serializer.data['folder_name']), many=True)

            temp_respond.append(len(img_serializer.data))
            return Response(temp_respond)

        # send compact data of chosen image to web
        else:
            try:
                page = int(type)
            except BaseException as error:
                print(error)
            else:
                folder_serializer = FolderImageSerializer(
                    Folder_img.objects.get(folder_id=folder_id)
                )

                img_serializer = ImageSerializer(
                    Image_file.objects.all().filter(user_id=payload['id'], img_folder=folder_serializer.data['folder_name']), many=True)

                chosen_range_min = (page-1) * 25
                chosen_range_max = page * 25
 
                for i in range(chosen_range_min,chosen_range_max):
                    file_type = (img_serializer.data[i]['img_type'].split('/'))[1]
                    try:
                        with Image.open('C:/IPAuTSoNS/backend/IPAutSoNsAPI'+str(img_serializer.data[i]['path'])) as image_file_temp:
                            percentage = 0.1
                            width, height = image_file_temp.size
                            resized_dimensions = (
                                int(width * percentage), int(height * percentage))
                            resized_image = image_file_temp.resize(
                                resized_dimensions)
                            buffer = BytesIO()
                            resized_image.save(buffer, format=file_type)
                            image_data = base64.b64encode(buffer.getvalue())

                            temp_img_data = {
                                'img_id': img_serializer.data[i]['img_id'],
                                'user_id': img_serializer.data[i]['user_id'],
                                'img_type': img_serializer.data[i]['img_type'],
                                'img_folder': img_serializer.data[i]['img_folder'],
                                'path': img_serializer.data[i]['path'],
                                'img_size': img_serializer.data[i]['img_size'],
                                'img_data': image_data
                            }
                            
                            temp_respond.append(temp_img_data)

                    except BaseException as error:
                        print(error)

            return Response(temp_respond)
                    




    # add image
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

    # delete image
    def delete(self, request, folder_id):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        img_id = folder_id
        image = Image_file.objects.get(img_id=img_id)
        try:
            os.remove('C:/IPAuTSoNS/backend/IPAutSoNsAPI/media/'+str(image.path))
        except BaseException as error:
            print(error)
            return Response({"status": "Delete fail ! try again"})
        else:
            image.delete()
            return Response({"status": "Delete done!"})


class AllImageView(APIView):
    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        serializer = ImageSerializer(
            Image_file.objects.all().filter(user_id=payload['id']), many=True)
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

    # send image folder
    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        serializer = FolderImageSerializer(
            Folder_img.objects.all().filter(user_id=payload['id']), many=True)
        return Response(serializer.data)

    # delete image folder
    def delete(self, request, folder_id):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        folder_img = Folder_img.objects.get(folder_id=folder_id)
        try:
            shutil.rmtree(os.path.join(str(folder_img.path)))
        except BaseException as error:
            print(error)
            return Response({"status": "Delete fail ! try again"})
        else:
            print(folder_img.folder_name)
            del_img = Image_file.objects.all().filter(img_folder=folder_img.folder_name)
            folder_img.delete()
            del_img.delete()

            return Response({"status": "Delete done !"})


class MakeDockerFile(APIView):
    def post(self, request):
        token = request.data['jwt']
        job_id = request.data['job_id']
        app_id = request.data['app_id']
        path = request.data['path']
        num_img = request.data['num_img']
        img_selected = request.data['img_selected']
        create_time = datetime.datetime.now()
        print(create_time)
        payload = Authentication(token)

        user = User.objects.get(user_id=payload['id'])

        template = """apiVersion: batch/v1
kind: Job
metadata:
    name: """+job_id+"""
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
