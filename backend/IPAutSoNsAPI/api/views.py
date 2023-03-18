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
from .models import Folder_img, Job, User, Image_file, Product, Login_log, Payment
from .serializers import JobSerializer, UserSerializer, ImageSerializer, FolderImageSerializer, ProductSerializer, PaymentSerializer
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
from yaml_run import YamlRunner
import logging

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))


class VersionCheck(APIView):
    def get(self,request):
        return Response({"version":"1.2:1521"})

# for Authentication user with JWT
def Authentication(token):
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'IPAutSoNs', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:

        raise AuthenticationFailed('Unauthenticated')

    return payload


def get_size(file_size, unit='bytes'):
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)


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
        elif not user.check_password(password):
            raise AuthenticationFailed("Password is not match!")
        else:
            payload = {
                'id': user.user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'IPAutSoNs', algorithm='HS256')

            respond = Response()
            # respond.set_cookie(key='jwt',value=token,httponly=True)
            respond.data = ({
                'jwt': token,
                'fname':user.first_name,
                'lname':user.last_name
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
                    with Image.open(str(BASE_DIR)+str(Path(i['path']))) as image_file_temp:
                        fixed_height = 200
                        height_percent = (
                            fixed_height / float(image_file_temp.size[1]))
                        width_size = int(
                            (float(image_file_temp.size[0]) * float(height_percent)))
                        resized_image = image_file_temp.resize(
                            (width_size, fixed_height))
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
                    with Image.open(str(BASE_DIR)+str(Path(i['path']))) as image_file_temp:
                        percentage = 1
                        resized_image = image_file_temp
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

            folder_size = 0

            img_serializer = ImageSerializer(
                Image_file.objects.all().filter(user_id=payload['id'], img_folder=folder_serializer.data['folder_name']), many=True)

            for i in img_serializer.data:
                folder_size += int(i['img_size'])

            print("folder size = "+str(get_size(folder_size, 'gb'))+" gb")

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

                chosen_range_min = (page-1) * 24
                chosen_range_max = page * 24

                for i in range(chosen_range_min, chosen_range_max):

                    try:
                        print('send img from here')
                        file_type = (img_serializer.data[i]['img_type'].split('/'))[1]
                        with Image.open(str(BASE_DIR)+str(Path(img_serializer.data[i]['path']))) as image_file_temp:
                            percentage = 0.25
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

    # add images

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
            del_path = os.path.join(BASE_DIR, "nas_sim/ipautsons", str(image.path))
            os.remove(del_path)
        except BaseException as error:
            print(error)
            return Response({"status": "Delete fail !!! try again"})
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
    # create ,new image folder
    def post(self, request):
        print(BASE_DIR)
        token = request.data['jwt']
        payload = Authentication(token)
        user_id = payload['id']
        folder_name = request.data['folder_name']
        folder_path = os.path.join(
            BASE_DIR, "nas_sim/ipautsons", user_id, "root", folder_name)

        try:
            os.makedirs(folder_path)
        except OSError as error:
            print(error)
            return Response({'status': '!!! Something is wrong try again !!!'})
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
            shutil.rmtree(folder_img.path)
        except BaseException as error:
            print(error)
            return Response({"status": "Delete fail ! try again"})
        else:
            print(folder_img.folder_name)
            del_img = Image_file.objects.all().filter(img_folder=folder_img.folder_name)
            folder_img.delete()
            del_img.delete()

            return Response({"status": "Delete done !"})


class ProductView(APIView):
    def get(self, request, product_id):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        return Response({"status": product_id})

    def post(self, request):
        token = request.META['HTTP_JWT']
        print(request)
        payload = Authentication(token)
        weight_file = request.FILES.get('weight_file')
        product_img = request.FILES.get('product_img')
        print(weight_file)
        print(product_img)
        product_data = {
            'product_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
            'user_id': payload['id'],
            'product_name': request.data['name'],
            'product_type': request.data['type'],
            'model': request.data['model'],
            'price': request.data['price'],
            'detail':request.data['detail'],
            'path': weight_file,
            'product_img': product_img,
            'last_update': datetime.datetime.utcnow()

        }

        try:
            serializer = ProductSerializer(data=product_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("file "+weight_file.name+" upload done")

        except (BaseException) as error:
            print(error)
            return Response({"status": "Fail to add product try again."})
        else:
            return Response({"status": "Add product successful"})


class PaymentView(APIView):
    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        serializer = PaymentSerializer(
            Payment.objects.all().filter(user_id=payload['id']), many=True)
        return Response(serializer.data)

    def post(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        payment_data = {
            'payment_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=25)),
            'product_id': request.data['product_id'],
            'user_id': payload['id'],
            'type': request.data['type'],
            'pay_time': datetime.datetime.utcnow()
        }
        try:
            serializer = PaymentSerializer(data=payment_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except (BaseException) as error:
            print(error)
            return Response({"status": "Fail to add payment try again."})
        else:
            return Response({"status": "Add payment successful"})


class MakeDockerFile(APIView):
    def post(self, request):
        logger.info('Running YAMLRunner at '+str(datetime.datetime.now()))
        # job_id = request.data['job_id']
        # token = request.META['HTTP_JWT']
        # path = request.data['path']
        # param1 = request.data['param1']
        # num_img = request.data['num_img']
        # img_selected = request.data['img_selected']
        # payload = Authentication(token)
        # user = User.objects.get(user_id=payload['id'])
        # path = "/ipautsons/backend/media"+path
        # img_folder_temp = path.split("/")
        # img_folder = img_folder_temp[5]

        template = """apiVersion: batch/v1

kind: Job

metadata:

  name: test123

spec:

  template:

    spec:

      containers:

      - name: test123

        image: suteesaraphan27/ascii
        volumeMounts:
            - name: nfs-share
              mountPath: /ipautsons

        command: ["python","ASCII.py","test123","/ipautsons/img"]

      restartPolicy: Never
      volumes:
      - name: nfs-share
        persistentVolumeClaim: 
          claimName: example"""
#         
#             job_data = {
#                 'job_id': job_id,
#                 'user_id': user.user_id,
#                 # 'app_id': app_id,
#                 'path': path,
#                 'num_img': num_img,
#                 'img_selected': img_selected,
#                 'job_status': "0"
#             }

#             serializer = JobSerializer(data=job_data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
        try:
            with open('yaml_file/'+"test123"+'.yaml', 'w') as yfile:
                yfile.write(template)
                yfile.close()
                logger.error('Calling run_yaml functions')
                yaml_run = YamlRunner()
                yaml_run.run_yaml()
            return Response({"status": "File is made!"})

        except (BaseException)as error:
            print(error)
            return Response({"status": "something is not right"})


# class MakeDockerFile(APIView):
#     def post(self, request):
#         job_id = request.data['job_id']
#         token = request.META['HTTP_JWT']
#         path = request.data['path']
#         param1 = request.data['param1']
#         num_img = request.data['num_img']
#         img_selected = request.data['img_selected']
#         payload = Authentication(token)
#         user = User.objects.get(user_id=payload['id'])
#         path = "/ipautsons/backend/media"+path
#         img_folder_temp = path.split("/")
#         img_folder = img_folder_temp[5]

#         template = """apiVersion: batch/v1
# kind: Job
# metadata:
#   name:"""+job_id+"""
# spec:
#   template:
#     spec:
#       containers:
#       - name: """+job_id+"""
#         image: suteesaraphan27/ascii
#         volumeMounts:
#             - name: myvolume
#               mountPath: /www
#         command: ["python","ASCII.py","""+img_folder+""","""+path+"""]
#       restartPolicy: Never
#       volumes:
#       - name: myvolume
#         persistentVolumeClaim: 
#           claimName: mypvc"""
#         try:
#             job_data = {
#                 'job_id': job_id,
#                 'user_id': user.user_id,
#                 # 'app_id': app_id,
#                 'path': path,
#                 'num_img': num_img,
#                 'img_selected': img_selected,
#                 'job_status': "0"
#             }

#             serializer = JobSerializer(data=job_data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#             with open('yaml_file/'+job_id+'.yaml', 'w') as yfile:
#                 yfile.write(template)
#                 yfile.close()
#                 yaml_run = YamlRunner(job_id)
#                 yaml_run.run_yaml()
#             return Response({"status": "File is made!"})

#         except (BaseException)as error:
#             print(error)
#             return Response({"status": "ERROR create job file fail"})
