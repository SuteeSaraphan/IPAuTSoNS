from ctypes import sizeof
from io import BytesIO
from operator import length_hint
import random
import shutil
import string
from time import sleep
from django.shortcuts import render
from requests import delete
from .models import Folder_img, Job, User, Image_file, Product, Login_log, Payment
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
import os
import base64
from pathlib import Path
from PIL import Image
from yaml_run import YamlRunner
from preview_api import PreviewAPI
from preview_adv_api import PreviewADVAPI
import logging
import requests
import json
from django.http import HttpResponse, Http404


PROCESS_TAX = 0.9
logger = logging.getLogger(__name__)


class VersionCheck(APIView):
    def get(self, request):
        return Response({"version": "1.11"})

# for Authentication user with JWT


def download_file(request, img_id):

    img_download = Image_file.objects.get(img_id=img_id)

    # Path to the file on the server
    file_path = os.path.join("ipautsons",img_download.path.path)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise Http404

    # Open the file as a binary object
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{img_id}"'
        return response

def download_folder(request, img_id):

    img_download = Image_file.objects.get(img_id=img_id)

    # Path to the file on the server
    file_path = os.path.join("ipautsons",img_download.path.path)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise Http404

    # Open the file as a binary object
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{img_id}"'
        return response

def Authentication(token):
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'IPAutSoNs', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:

        raise AuthenticationFailed('Unauthenticated')

    return payload


def storage_size(user_id):
    folder_size = 0
    folder_serializer = FolderImageSerializer(
        Folder_img.objects.all().filter(user_id=user_id), many=True)

    for i in folder_serializer.data:
        img_serializer = ImageSerializer(Image_file.objects.all().filter(
            user_id=user_id, img_folder=i['folder_name']), many=True)

        for j in img_serializer.data:
            folder_size += int(j['img_size'])

    return get_size(folder_size, 'gb')


def get_size(file_size, unit='bytes'):
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)


def add_credit(payment_id,user_id, credit, product_id=None):
    payment_data = {
        'payment_id': payment_id,
        'product_id': product_id,
        'user_id': user_id,
        'type': 0,
        'credit': credit,
        'pay_time': datetime.datetime.utcnow()
    }
    try:
        serializer = PaymentSerializer(data=payment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return 1
    except Exception as error:
        return error


def sub_credit(payment_id,user_id, credit, product_id=None):
    payment_data = {
        'payment_id': payment_id,
        'product_id': product_id,
        'user_id': user_id,
        'type': 1,
        'credit': credit,
        'pay_time': datetime.datetime.utcnow()
    }
    try:
        serializer = PaymentSerializer(data=payment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return 1
    except Exception as error:
        return error

def del_payment(payment_id):
    payment_to_del = Payment.objects.get(payment_id = payment_id)
    payment_to_del.delete()
    print("del payment compl :" +payment_id)
    return False
       

def credit_check(user_id):
    all_payment = Payment.objects.all().filter(
        user_id=user_id).order_by('pay_time')
    credit_total = 0
    # type 0 = + # type 1 = -
    for i in all_payment:
        if (i.type == '0'):
            credit_total += i.credit
        elif (i.type == '1'):
            credit_total -= i.credit

    return credit_total

# for doing register new user

def discount_calculate(num_img):
    if(num_img>=1000):
            return 0.1
    elif(num_img>=500):
            return 0.25
    elif(num_img>=250):
            return 0.40
    elif(num_img>=100):
            return 0.50
    elif(num_img>=50):
            return 0.75
    elif(num_img>=25):
            return 0.90
    else:
        return 1


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        add_credit_result = add_credit(''.join(random.choices(
            string.ascii_lowercase + string.digits, k=25)),request.data['user_id'], 1000, 0)
        if (add_credit_result != 1):
            Response(data={"status": "ERROR Register fail ",
                     "cause": str(add_credit_result)}, status=503)
        return Response(serializer.data)

# for user login


class LoginView(APIView):
    def post(self, reqest):
        email = reqest.data['email']
        password = reqest.data['password']
        user = None
        try:
            user = User.objects.get(email=email)
        except Exception as error:
            print(error)
        if user is None:
            return Response(status=404)
        elif not user.check_password(password):
            return Response(status=404)
        else:
            payload = {
                'id': user.user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'IPAutSoNs', algorithm='HS256')
            folder_size = storage_size(user.user_id)
            credit = credit_check(user.user_id)
            respond = Response()
            # respond.set_cookie(key='jwt',value=token,httponly=True)
            respond.data = ({
                'jwt': token,
                'fname': user.first_name,
                'lname': user.last_name,
                'storage': folder_size,
                'credit': credit
            })

            login_log = ({
                'login_log_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=15)),
                'user_id': user.user_id,
                'login_time': datetime.datetime.utcnow()
            })

            serializer = Login_logSerializer(data=login_log)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
                    with Image.open(str(Path(i['path']))) as image_file_temp:  # depoly
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
                    logger.error(error)

            return Response(temp_respond)

        # send full data of one image to web
        elif (type == 'once'):
            img_serializer = ImageSerializer(
                Image_file.objects.get(img_id=folder_id))
            file_type = (img_serializer.data['img_type'].split('/'))[1]
            if (file_type.lower() == 'jpg' or file_type.lower() == 'jpeg'):
                file_type = 'jpeg'
            else:
                file_type = 'png'
            try:
                # deploy
                with Image.open(str(Path(img_serializer.data['path']))) as image_file_temp:
                    buffer = BytesIO()
                    image_file_temp.save(buffer, format=file_type)
                    image_data = base64.b64encode(buffer.getvalue())
                    temp_img_data = {
                        'img_id': img_serializer.data['img_id'],
                        'user_id': img_serializer.data['user_id'],
                        'img_type': img_serializer.data['img_type'],
                        'img_folder': img_serializer.data['img_folder'],
                        'path': img_serializer.data['path'],
                        'img_size': img_serializer.data['img_size'],
                        'img_data': image_data
                    }
                    temp_respond.append(temp_img_data)
                return Response(temp_respond)

            except BaseException as error:
                print(error)
                logger.error(error)
                return Response(data={'status': 'something wrong'}, status=503)

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
                        file_type = (
                            img_serializer.data[i]['img_type'].split('/'))[-1]
                        if (file_type.lower() == "jpg" or file_type.lower() == "jpeg"):
                            file_type = "jpeg"
                        else:
                            file_type = "png"

                        # deploy
                        with Image.open(str(Path(img_serializer.data[i]['path']))) as image_file_temp:
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
                        logger.error(error)

            return Response(temp_respond)

    # add images

    def post(self, request):
        token = request.data['jwt']
        folder = request.data['folder']
        payload = Authentication(token)
        user = User.objects.get(user_id=payload['id'])
        try:
            print("------------------")
            img_data = {
                'img_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
                'user_id': user.user_id,
                'img_type': request.FILES['img_file'].content_type,
                'img_folder': folder,
                'path': request.FILES['img_file'],
                'img_size': request.FILES['img_file'].size
            }
            serializer = ImageSerializer(data=img_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as error:
            print(error)
            logger.error(error)
            return Response(data={"status": "file "+request.FILES['img_file'].name+" upload fail"}, status=503)
        else:
            return Response({"status": "file "+request.FILES['img_file'].name+" upload done"})

    # delete image
    def delete(self, request, folder_id):
        print("run")
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        img_id = folder_id
        image = Image_file.objects.get(img_id=img_id)
        try:
            del_path = "/ipautsons/"+str(image.path)  # deploy
            
            os.remove(del_path)
        except BaseException as error:
            print(error)
            return Response(data={"status": "Delete fail !!! try again","cause":str(error)}, status=503)
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
        token = request.data['jwt']
        payload = Authentication(token)
        user_id = payload['id']
        folder_name = request.data['folder_name']
        folder_path = os.path.join(
            "ipautsons", user_id, "root", folder_name)  # deploy
        try:
            os.makedirs("/"+folder_path)
        except OSError as error:
            print(error)
            return Response(data={'status': 'ERROR481 Create folder fail !!!'}, status=503)
        else:
            folder_data = {
                'folder_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
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
            shutil.rmtree("/"+folder_img.path)
        except BaseException as error:
            print(error)
            return Response(data={"status": "Delete fail ! try again", "cause": str(error)}, status=503)
        else:
            del_img = Image_file.objects.all().filter(img_folder=folder_img.folder_name)
            folder_img.delete()
            del_img.delete()

            return Response({"status": "Delete done !"})


class FeedView(APIView):
    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        temp_respond = []
        product = ProductSerializer(
            Product.objects.all().order_by('-last_update')[:12], many=True)
        for i in product.data:
            file_type = (i['product_img'].split('.'))[-1]
            seller = User.objects.get(user_id=i['user_id'])
            if (file_type == 'JPG' or file_type == 'JPEG' or file_type == 'jpg' or file_type == 'jpeg'):
                file_type = 'jpeg'
            else:
                file_type = 'png'
            try:
                with Image.open(str(Path(i['product_img']))) as image_file_temp:  # deploy
                    percentage = 0.25
                    width, height = image_file_temp.size
                    resized_dimensions = (
                        int(width * percentage), int(height * percentage))
                    resized_image = image_file_temp.resize(
                        resized_dimensions)
                    buffer = BytesIO()
                    resized_image.save(buffer, format=file_type)
                    image_data = base64.b64encode(buffer.getvalue())

                    temp_product_data = {
                        'product_id': i['product_id'],
                        'product_name': i['product_name'],
                        'seller': seller.first_name + " " + seller.last_name,
                        'product_type': i['product_type'],
                        'model': i['model'],
                        'price': i['price'],
                        'detail': i['detail'],
                        'product_img': image_data,
                        'last_update': i['last_update']
                    }
                    temp_respond.append(temp_product_data)

            except Exception as error:
                print(error)
        return Response(temp_respond)


class ProductView(APIView):#----------------สินค้า--------------------
    def get(self, request, type, key):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)

        if (type == 'once'):
            try:
                product = ProductSerializer(
                    Product.objects.get(product_id=key))
            except Exception as error :
                return Response({"status":"Can't find product,try again"},status=503)
            ownner = UserSerializer(User.objects.get(
                user_id=product.data['user_id']))

            file_type = (product.data['product_img'].split('.'))[-1]

            if (file_type.lower() == 'jpg' or file_type.lower() == 'jpeg'):
                file_type = 'jpeg'
            else:
                file_type = 'png'
            # deploy
            with Image.open(str(Path(product.data['product_img']))) as image_file_temp:
                percentage = 0.25
                width, height = image_file_temp.size
                resized_dimensions = (
                    int(width * percentage), int(height * percentage))
                resized_image = image_file_temp.resize(
                    resized_dimensions)
                buffer = BytesIO()
                resized_image.save(buffer, format=file_type)
                image_data = base64.b64encode(buffer.getvalue())

            is_ownner = (product.data['user_id'] == payload['id'])
            response = Response({
                'is_ownner': is_ownner,
                'product_id': product.data['product_id'],
                'product_name': product.data['product_name'],
                'product_type': product.data['product_type'],
                'model': product.data['model'],
                'ownner': ownner.data['first_name'] + " " + ownner.data['last_name'],
                'last_update': product.data['last_update'],
                'detail': product.data['detail'],
                'product_img': image_data,
                'product_price': product.data['price'],
            })

            return response

        elif (type == 'img_app'):

            product = ProductSerializer(
                Product.objects.get(product_id=key))
            return Response(product.data)

    def put(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        product_edit = Product.objects.get(product_id=request.data['id'])
        product_edit.product_name = request.data['name']
        product_edit.product_type = request.data['type']
        product_edit.model = request.data['model']
        product_edit.price = request.data['price']
        product_edit.detail = request.data['detail']
        product_edit.last_update = datetime.datetime.utcnow()

        try:
            weight_file = request.FILES.get('weight_file')
        except Exception:
            pass
        else:
            if (weight_file != None):
                product_edit.path = weight_file

        try:
            product_img = request.FILES.get('product_img')
        except Exception:
            pass
        else:
            if (product_img != None):
                product_edit.product_img = product_img

        try:
            product_edit.save()
        except (Exception) as error:
            print(error)
            return Response(data={"status": "Fail to edit product try again."}, status=503)
        else:
            return Response({"status": "Edit product successful"})

    def post(self, request):
        token = request.META['HTTP_JWT']
        print(request)
        payload = Authentication(token)
        try:
            weight_file = request.FILES.get('weight_file')
            product_img = request.FILES.get('product_img')
            product_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            product_data = {
                'product_id': product_id,
                'user_id': payload['id'],
                'product_name': request.data['name'],
                'product_type': request.data['type'],
                'model': request.data['model'],
                'price': request.data['price'],
                'detail': request.data['detail'],
                'path': weight_file,
                'product_img': product_img,
                'last_update': datetime.datetime.utcnow()

            }

            serializer = ProductSerializer(data=product_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            try:
                product = Product.objects.get(product_id=product_id)
                with open(str(Path(product.product_img.path)), 'rb') as image_file:
                    weight_checker_api_url = 'http://192.168.1.46:'
                    if(product.model=='YOLOv5'):
                        weight_checker_api_url = weight_checker_api_url+'4050/weight-checker?modelse='
                        headers = {'accept': 'application/json'}
                        files = {'file': image_file}
                        weight_checker_api_url =  weight_checker_api_url+str(product.path.path)

                        response = requests.post(weight_checker_api_url, headers=headers ,files=files)
                        logger.error('response.text : '+str(response.text))
                        res = json.loads(response.text)
                        if(res['msg']=="OK"):
                            return Response(data={"status": "Add new product success is made!"})
                        else:
                            logger.error('product add error because : '+str(res['msg']))
                            product.delete()
                            return Response(data={'status': 'ERROR695 Export job fail !!!','cause':"server issue"}, status=503)
                        
                    elif(product.model=='GANs'):
                        weight_checker_api_url = weight_checker_api_url+'4070/gan?modelse='
                        headers = {'accept': 'application/json'}
                        files = {'file': image_file}
                        weight_checker_api_url =  weight_checker_api_url+str(product.path.path)
                        
                        response = requests.post(weight_checker_api_url, headers=headers ,files=files)
                        try:
                            logger.error(response.content)
                            logger.error(type(response.content))
                            image_data = Image.open(BytesIO(response.content))
                            
                        except Exception as error:
                            logger.error('product add error because : '+str(error))
                            product.delete()
                            return Response(data={'status': 'ERROR695 Export job fail !!!','cause':"server issue"}, status=503)
                        else:
                            return Response(data={"status": "Add new product success is made!"})
                    

            except Exception as error:
                product.delete()
                print(str(error))
                logger.error(str(error))
                return Response(data={"status": "Fail to add product try again.","cause":"701"+str(error)}, status=503)
            
        except (Exception) as error:
            print(str(error))
            logger.error(str(error))
            return Response(data={"status": "Fail to add product try again.","cause":"706"+str(error)}, status=503)
        


class MarketView(APIView):

    def get(self, request, key):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)

        product_type, model, sort = str(key).split("_")

        if (product_type == "All" and model == "All"):
            if (sort == 'newest'):
                all_product = ProductSerializer(
                    Product.objects.all().order_by('-last_update'), many=True)
            elif (sort == 'oldest'):
                all_product = ProductSerializer(
                    Product.objects.all().order_by('last_update'), many=True)

        elif (product_type != "All" and model != "All"):
            if (sort == 'newest'):
                all_product = ProductSerializer(
                    Product.objects.all().filter(model=model).filter(product_type=product_type).order_by('-last_update'), many=True)
            elif (sort == 'oldest'):
                all_product = ProductSerializer(
                    Product.objects.all().filter(model=model).filter(product_type=product_type).order_by('last_update'), many=True)

        elif (product_type != "All" and model == "All"):
            if (sort == 'newest'):
                all_product = ProductSerializer(
                    Product.objects.all().filter(product_type=product_type).order_by('-last_update'), many=True)
            elif (sort == 'oldest'):
                all_product = ProductSerializer(
                    Product.objects.all().filter(product_type=product_type).order_by('last_update'), many=True)

        elif (product_type == "All" and model != "All"):
            if (sort == 'newest'):
                all_product = ProductSerializer(
                    Product.objects.all().filter(model=model).order_by('-last_update'), many=True)
            elif (sort == 'oldest'):
                all_product = ProductSerializer(
                    Product.objects.all().filter(model=model).order_by('last_update'), many=True)

        temp_respond = []
        for i in all_product.data:
            file_type = (i['product_img'].split('.'))[-1]
            seller = User.objects.get(user_id=i['user_id'])
            if (file_type == 'JPG' or file_type == 'JPEG' or file_type == 'jpg' or file_type == 'jpeg'):
                file_type = 'jpeg'
            else:
                file_type = 'png'
            try:
                with Image.open(str(Path(i['product_img']))) as image_file_temp:  # deploy
                    percentage = 0.25
                    width, height = image_file_temp.size
                    resized_dimensions = (
                        int(width * percentage), int(height * percentage))
                    resized_image = image_file_temp.resize(resized_dimensions)
                    buffer = BytesIO()
                    resized_image.save(buffer, format=file_type)
                    image_data = base64.b64encode(buffer.getvalue())

                    temp_img_data = {
                        'product_id': i['product_id'],
                        'product_name': i['product_name'],
                        'seller': seller.first_name + " " + seller.last_name,
                        'product_type': i['product_type'],
                        'model': i['model'],
                        'price': i['price'],
                        'detail': i['detail'],
                        'product_img': image_data,
                        'last_update': i['last_update']
                    }
                    temp_respond.append(temp_img_data)

            except Exception as error:
                print(error)

        return Response(temp_respond)

#--------------------------------open product-------------------------------------

class OpenProductView(APIView):
    def post(seld, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        user = User.objects.get(user_id=payload['id'])
        product = Product.objects.get(product_id=request.data['product_id'])

        try:
            Open_product.objects.get(product_id=request.data['product_id'],user_id=payload['id'])
        except:
            open_product_data ={
            'open_product_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
            'user_id' : user.user_id,
            'product_id' : product.product_id
            }

            serializer = OpenProductSerializer(data=open_product_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"status": "Open product success"})
        else:
            return Response({"status": "Open product fail",'cause':'product is already turn on'},status=503)
            
        

    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        openProducts = OpenProductSerializer(Open_product.objects.all().filter(user_id=payload['id']), many=True)
        temp_respond = []
        for i in openProducts.data:
            product_temp = Product.objects.get(product_id=i['product_id'])
            openProduct_temp ={
                'product_id': product_temp.product_id,
                'product_name': product_temp.product_name,
                'model': product_temp.model
            }
            temp_respond.append(openProduct_temp)
        return Response(temp_respond)

#---------------------------------PREVIEW-----------------------------------------
class PreviewNormalView(APIView):
    def post(seld, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        # preview = PreviewAPI(request.data['img_id'],request.data['product_id'],request.data['product_value'])
        img_serializer = ImageSerializer(
            Image_file.objects.get(img_id=request.data['img_id']))
        file_type = (img_serializer.data['img_type'].split('/'))[1]
        try:
            # deploy
            with open(str(Path(img_serializer.data['path'])), 'rb') as image_file:
                preview = PreviewAPI(
                    image_file, file_type, request.data['product_id'], request.data['product_value'])
                img_preview = preview.do_preview()
                image_data = Image.open(BytesIO(img_preview))
                buffer = BytesIO()
                image_data.save(buffer, format=file_type)
                image_data = base64.b64encode(buffer.getvalue())
                temp_img_data = {
                    'img_id': img_serializer.data['img_id'],
                    'user_id': img_serializer.data['user_id'],
                    'img_type': img_serializer.data['img_type'],
                    'img_folder': img_serializer.data['img_folder'],
                    'path': img_serializer.data['path'],
                    'img_size': img_serializer.data['img_size'],
                    'img_data': image_data
                }
                return Response(temp_img_data)

        except Exception as error:
            print(error)
            return Response(data={'status': str(error)}, status=503)

#---------------------------------PREVIEW-ADV-----------------------------------------
class PreviewAdvanceView(APIView):
    def post(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        # preview = PreviewAPI(request.data['img_id'],request.data['product_id'],request.data['product_value'])
        product_on_job = Product.objects.get(product_id=request.data['product_id'])
        product_on_job_path = product_on_job.path.path
        img_serializer = ImageSerializer(Image_file.objects.get(img_id=request.data['img_id']))
        file_type = (img_serializer.data['img_type'].split('/'))[1]
        logger.error('start preview ADV')
        logger.error(str(Path(img_serializer.data['path'])))
        try:
            # deploy
            logger.error('1')
            with open(str(Path(img_serializer.data['path'])), 'rb') as image_file:
                logger.error('2')
                preview = PreviewADVAPI(
                    image_file, file_type, product_on_job.model, product_on_job_path)
                print('call do_preview')
                img_preview = preview.do_preview()

                image_data = Image.open(BytesIO(img_preview))
                buffer = BytesIO()
                image_data.save(buffer, format=file_type)
                image_data = base64.b64encode(buffer.getvalue())
                temp_img_data = {
                    'img_id': img_serializer.data['img_id'],
                    'user_id': img_serializer.data['user_id'],
                    'img_type': img_serializer.data['img_type'],
                    'img_folder': img_serializer.data['img_folder'],
                    'path': img_serializer.data['path'],
                    'img_size': img_serializer.data['img_size'],
                    'img_data': image_data
                }
                return Response(temp_img_data)

        except Exception as error:
            logger.error("error 867"+str(error))
            return Response(data={'status': str(error)}, status=503)
        

class UserHistoryView(APIView):
    def get(self, request, type):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        record_total = 0
        match type:
            case 'newest':
                serializer = PaymentSerializer(
                    Payment.objects.all().filter(user_id=str(payload['id'])).order_by('-pay_time'), many=True
                )
                for i in serializer.data:
                    record_total += 1
            case 'oldest':
                serializer = PaymentSerializer(
                    Payment.objects.all().filter(user_id=str(payload['id'])).order_by('pay_time'), many=True
                )
                for i in serializer.data:
                    record_total += 1
            case _:
                date_search = str(type).split("-")
                print(date_search)
                serializer = PaymentSerializer(
                    Payment.objects.all()
                    .filter(user_id=str(payload['id']))
                    .filter(pay_time__gte=datetime.date(int(date_search[0]), int(date_search[1]), int(date_search[2])))
                    .order_by('pay_time'), many=True
                )
                for i in serializer.data:
                    record_total += 1
        if (record_total > 0):
            return Response(serializer.data)
        else:
            return Response({'status': 'no record found'}, status=503)
        

class JobHistoryView(APIView):
    def get(self, request, type):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        record_total = 0
        match type:
            case 'newest':
                serializer = JobSerializer(
                    Job.objects.all().filter(user_id=str(payload['id'])).order_by('-create_time'), many=True
                )
                for i in serializer.data:
                    record_total += 1
            case 'oldest':
                serializer = JobSerializer(
                    Job.objects.all().filter(user_id=str(payload['id'])).order_by('create_time'), many=True
                )
                for i in serializer.data:
                    record_total += 1
            case _:
                date_search = str(type).split("-")
                print(date_search)
                serializer = JobSerializer(
                    Job.objects.all()
                    .filter(user_id=str(payload['id']))
                    .filter(create_time__gte=datetime.date(int(date_search[0]), int(date_search[1]), int(date_search[2])))
                    .order_by('create_time'), many=True
                )
                for i in serializer.data:
                    record_total += 1
        if (record_total > 0):
            return Response(serializer.data)
        else:
            return Response({'status': 'no record found'}, status=503)


class PaymentView(APIView):
    def get(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        serializer = PaymentSerializer(
            Payment.objects.all().filter(user_id=str(payload['id'])).order_by('pay_time'), many=True
        )
        return Response(serializer.data)

    def post(self, request):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        user = User.objects.get(user_id=payload['id'])
        payment_data = {
            'payment_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=25)),
            'product_id': request.data['product_id'],
            'user_id': user,
            'type': request.data['type'],
            'credit': request.data['credit'],
            'pay_time': datetime.datetime.utcnow()
        }
        try:
            serializer = PaymentSerializer(data=payment_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except (BaseException) as error:
            print(error)
            return Response(data={"status": "Fail to add payment try again."}, status=503)
        else:
            return Response({"status": "Add payment successful"})


class ProductHistoryView(APIView):
    def get(self, request, product_id, type):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        record_total = 0
        if (type == 'newest'):
            serializer = PaymentSerializer(
                Payment.objects.all().filter(product_id=product_id).order_by('-pay_time'), many=True
            )
            for i in serializer.data:
                record_total += 1
        elif (type == 'oldest'):
            serializer = PaymentSerializer(
                Payment.objects.all().filter(product_id=product_id).order_by('pay_time'), many=True
            )
            for i in serializer.data:
                record_total += 1
        else:
            date_search = str(type).split("-")
            print(date_search)
            serializer = PaymentSerializer(
                Payment.objects.all()
                .filter(product_id=product_id)
                .filter(pay_time__gte=datetime.date(int(date_search[0]), int(date_search[1]), int(date_search[2])))
                .order_by('pay_time'), many=True
            )
            for i in serializer.data:
                record_total += 1

        if (record_total > 0):
            return Response(serializer.data)
        else:
            return Response({'status': 'no record found'}, status=503)

class PriceCheckView(APIView):
    def get(self,request,product_id,folder_name):
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        try:
            user = User.objects.get(user_id=payload['id'])
        except Exception:
            return Response({'status': 'no record found'}, status=503)
        try:
            product = Product.objects.get(product_id = product_id)
            product_price = product.price
        except Exception as error :
            product_price = 5
        num_img_in_folder = Image_file.objects.all().filter(user_id=payload['id'], img_folder=folder_name).count()
        print(num_img_in_folder)
        discount = discount_calculate(num_img_in_folder)
        total_price = product_price*num_img_in_folder*discount

        if (credit_check(user)<total_price):
            return Response({'status': "Don't have enough credit"}, status=503) 
        else:
            return Response({'total_price':total_price})
#--------------------------------------------------------------YOLO------------------------------------------------
class YoloExport(APIView):
    def post(self,request):
        logger.error('Running Yolo api export at '+str(datetime.datetime.now()))
        print("product_id : " + str(request.data['product_id']))
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        user = User.objects.get(user_id=payload['id'])
        buyyer_payment_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=25))
        seller_payment_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=25))
        
        job_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=15))
        

        yolo_api_url = 'http://192.168.1.46:4050/detect?'

        img_sel = Image_file.objects.get(img_id=request.data['img_id'])
        img_selected = img_sel.img_id
        img_path = str(img_sel.path)
        img_path = img_path.split('/')

        num_img = Image_file.objects.all().filter(
            user_id=payload['id']).filter(img_folder=img_path[2]).count()
        add_result = None
        sub_result = None
        product_on_job = None

        try:
            product_on_job = Product.objects.get(product_id=request.data['product_id'])
        except Exception as err:
            return Response(data={"status": "ERROR1014 Export job fail", "cause": str(err)}, status=503)
        

        discount = discount_calculate(num_img)
        total_credit_use = (int(num_img)*product_on_job.price)*float(discount)
        user_credit = credit_check(user)
        if (user_credit < total_credit_use):
            return Response(data={"status": "ERROR1016 Export job fail", "cause": "Do not have enough credit point"}, status=503)
        try:
            sub_result = sub_credit(
            buyyer_payment_id,user, total_credit_use, product_on_job.product_id)
            add_result = add_credit(seller_payment_id,product_on_job.user_id, (total_credit_use)*0.9, product_on_job.product_id)
        except Exception as err:
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                    pass
            return Response(data={"status": "ERROR1031 Export job fail", "cause": str(err)}, status=503)
        
        if (sub_result != 1  or add_result != 1):
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                    pass
            return Response(data={"status": "ERROR1059 Export job fail", "cause": str(add_result)+" and "+str(sub_result)}, status=503)

        path = "/ipautsons/"+img_path[0]+"/"+img_path[1]+"/"+img_path[2]

        prodcut_name_no_space = product_on_job.product_name.replace(' ','-')
        docker_image_name = prodcut_name_no_space
        now = datetime.datetime.now()
        time_now = now.strftime("%H")+now.strftime("%M")+now.strftime("%S")
        result_folder_name = img_path[2]+'-'+prodcut_name_no_space+'-'+time_now
        result_path = "ipautsons/"+img_path[0]+"/"+img_path[1]+"/"+result_folder_name

        try:
            os.makedirs("/"+result_path)
        except Exception as error:
            print(error)
            return Response(data={'status': 'ERROR1085 Create folder fail !!!','cause':str(error)}, status=503)
        else:
            try:
                folder_data = {
                    'folder_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
                    'user_id': payload['id'],
                    'folder_name': result_folder_name,
                    'path': result_path,
                    'is_hidden': False
                }

                serializer = FolderImageSerializer(data=folder_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as error:
                print(error)
                buyyer_payment_del_sta = True
                seller_payment_del_sta = True
                while(buyyer_payment_del_sta or seller_payment_del_sta ):
                    try:
                        buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                        seller_payment_del_sta = del_payment(seller_payment_id)
                    except :
                        pass
                return Response(data={'status': 'ERROR1101 Create folder fail !!!','cause':str(error)}, status=503)
        
#job_id=p5mltrbi9ar-test-test-1619&useridparam=p5mltrbi9ar&folders=%2Fipautsons%2Fp5mltrbi9ar%2Froot%2Ftest&modelse=yolov5n.pt&newfolder=%2Fipautsons%2Fp5mltrbi9ar%2Froot%2Ftest-testyolo'
        yolo_api_url = yolo_api_url+"job_id="+job_id+"&useridparam="+payload['id']+"&folders="+path+"&modelse="+product_on_job.path.path+"&newfolder=/"+result_path
        headers = {'accept': 'application/json'}
        try:
            job_data = {
                    'job_id': job_id,
                    'user_id': user.user_id,
                    'path': path,
                    'num_img': num_img,
                    'img_selected': img_selected,
                    'job_status': "0",
                    'product_id': product_on_job.product_id,
                    'payment_id': buyyer_payment_id
            }
            serializer = JobSerializer(data=job_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response = requests.post(yolo_api_url, headers=headers)
        except Exception as error:
            logger.error('error : '+str(error))
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                    pass
            return Response(data={'status': 'ERROR1089 Export job fail !!!','cause':str(error)}, status=503)
        logger.error('response.text : '+str(response.text))
        res = json.loads(response.text)

        if(res['msg']=="OK"):
            return Response(data={"status": "File is made!","credit_left":credit_check(user.user_id)})
        else:
            logger.error('yolo error because : '+str(res['msg']))
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                    pass
            return Response(data={'status': 'ERROR1089 Export job fail !!!','cause':"server issue"}, status=503)
#----------------------------------------------GAN-----------------------------------------------
class GanExport(APIView):
    def post(self, request):
        logger.error('Running GAN export file at '+str(datetime.datetime.now()))
        print("product_id : " + str(request.data['product_id']))
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        user = User.objects.get(user_id=payload['id'])
        buyyer_payment_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=25))
        seller_payment_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=25))

        job_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=15))
        img_sel = Image_file.objects.get(img_id=request.data['img_id'])
        img_selected = img_sel.img_id
        img_path = str(img_sel.path)
        img_path = img_path.split('/')

        num_img = Image_file.objects.all().filter(
            user_id=payload['id']).filter(img_folder=img_path[2]).count()
        add_result = None
        sub_result = None
        product_on_job = None
        logger.error('1187')

        try:
            product_on_job = Product.objects.get(product_id=request.data['product_id'])
        except Exception as error:
            return Response(data={"status": "ERROR1012 Export job fail", "cause": "Product loading fail"}, status=503)
        discount = discount_calculate(num_img)
        total_credit_use = (int(num_img)*product_on_job.price)*float(discount)
        user_credit = credit_check(user)
        
        if (user_credit < total_credit_use):
            return Response(data={"status": "ERROR1032 Export job fail", "cause": "Do not have enough credit point"}, status=503)
        
        try:
            sub_result = sub_credit(
                buyyer_payment_id,user, total_credit_use, product_on_job.product_id)
            add_result = add_credit(
                seller_payment_id,product_on_job.user_id, total_credit_use, product_on_job.product_id)
        except Exception as err:
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                        pass
            return Response(data={"status": "ERROR1074 Export job fail", "cause": str(err)}, status=503)
        
        logger.error('1223')
        logger.error('sub_result : ' +str(sub_result))
        logger.error('add_result : ' +str(add_result))
        if (sub_result != 1  or add_result != 1):
                buyyer_payment_del_sta = True
                seller_payment_del_sta = True
                while(buyyer_payment_del_sta or seller_payment_del_sta):
                    try:
                        buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                        seller_payment_del_sta = del_payment(seller_payment_id)
                    except :
                        pass
                return Response(data={"status": "ERROR1059 Export job fail", "cause": str(add_result)+" and "+str(sub_result)}, status=503)
        logger.error('1235')

        path = "/ipautsons/"+img_path[0]+"/"+img_path[1]+"/"+img_path[2]
        now = datetime.datetime.now()
        time_now = now.strftime("%H")+now.strftime("%M")+now.strftime("%S")
        
        result_folder_name = img_path[2]+'-'+product_on_job.product_name.replace(" ","-")+'-'+time_now
        result_path = "ipautsons/"+img_path[0]+"/"+img_path[1]+"/"+result_folder_name.replace(" ","-")
        docker_image_name = "gangen"
        in_command_file_name = '"'+"main.py"+'"'

        logger.error('1245')
        try:
            os.makedirs("/"+result_path)
        except Exception as error:
            print(error)
            return Response(data={'status': 'ERROR1250 Create folder fail !!!','cause':str(error)}, status=503)
        
        logger.error('1251')
        try:
            folder_data = {
                'folder_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
                'user_id': payload['id'],
                'folder_name': result_folder_name,
                'path': result_path,
                'is_hidden': False
            }

            serializer = FolderImageSerializer(data=folder_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as error:
            print(error)
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                        pass
            return Response(data={'status': 'ERROR1266 Create folder fail !!!','cause':str(error)}, status=503)
        
        logger.error('1277')
        name_job = '"'+user.first_name+'-'+img_path[2]+'-'+product_on_job.product_name.replace(" ","-")+'-'+str(time_now)+'"'
        path_temp = '"'+path+'"'
        result_path_temp = '"/'+result_path+'"'
        user_id_temp = '"'+str(payload['id'])+'"'
        weight_path_temp = '"'+product_on_job.path.path+'"'
        logger.error('1282')
        name_job = name_job.lower()

        template = """apiVersion: batch/v1

kind: Job

metadata:

  name: """+str(name_job)+"""

spec:

  template:

    spec:

      containers:

      - name: """+str(name_job)+"""

        image: suteesaraphan27/"""+str(docker_image_name)+"""
        volumeMounts:
            - name: nfs-share
              mountPath: /ipautsons

        command: ["python","""+str(in_command_file_name)+""","""+str(job_id)+""","""+str(user_id_temp)+""","""+str(path_temp)+""","""+str(result_path_temp)+""","""+str(weight_path_temp)+"""]

      restartPolicy: Never
      volumes:
      - name: nfs-share
        persistentVolumeClaim: 
          claimName: example"""
        
        job_data = {
                'job_id': job_id,
                'user_id': user.user_id,
                'path': path,
                'num_img': num_img,
                'img_selected': img_selected,
                'job_status': "0",
                'product_id': product_on_job.product_id,
                'payment_id': buyyer_payment_id
            }
        logger.error('1325')
        try:
            serializer = JobSerializer(data=job_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as error:
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                    pass
            return Response(data={"status": "ERROR1175 Export job fail", "cause": str(error)}, status=503)
    
        logger.error('1341')
        try:

            with open('yaml_file/'+job_id+'.yaml', 'w') as yfile:
                yfile.write(template)
                yfile.close()
                yaml_run = YamlRunner(job_id)
                x = yaml_run.run_yaml()
            if (x == 1):
                credit_check(user.user_id)
                return Response(data={"status": "File is made!","credit_left":credit_check(user.user_id)})
            else:
                buyyer_payment_del_sta = True
                seller_payment_del_sta = True
                while(buyyer_payment_del_sta or seller_payment_del_sta ):
                    try:
                        buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                        seller_payment_del_sta = del_payment(seller_payment_id)
                    except :
                        pass
                return Response(data={"status": "ERROR1377 Export job fail", "cause": str(x)}, status=503)
        except Exception as error:
            print(error)
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                    pass
            return Response(data={"status": "ERROR1206 Export job fail", "cause": str(error)}, status=503)

#---------------------------------------------BASIC----------------------------------------------
class MakeDockerFile(APIView):
    def post(self, request):
        logger.error('Running YAMLRunner at '+str(datetime.datetime.now()))
        print("product_id : " + str(request.data['product_id']))
        token = request.META['HTTP_JWT']
        payload = Authentication(token)
        user = User.objects.get(user_id=payload['id'])
        buyyer_payment_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=25))
        seller_payment_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=25))

        job_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=15))
        img_sel = Image_file.objects.get(img_id=request.data['img_id'])
        img_selected = img_sel.img_id
        img_path = str(img_sel.path)
        img_path = img_path.split('/')

        num_img = Image_file.objects.all().filter(
            user_id=payload['id']).filter(img_folder=img_path[2]).count()
        add_result = None
        sub_result = None
        product_on_job = None
        logger.error('1187')
        try:
            product_on_job = Product.objects.get(
                product_id=request.data['product_id'])
        except Exception as error:
            product_on_job = None
            discount = discount_calculate(num_img)
            total_credit_use = (int(num_img)*5)*float(discount)
            user_credit = credit_check(user)
            if (user_credit < total_credit_use):
                return Response(data={"status": "ERROR1012 Export job fail", "cause": "Do not have enough credit point"}, status=503)
            try:
                sub_result = sub_credit(buyyer_payment_id,user, total_credit_use, 0)
                add_result = add_credit(seller_payment_id,"ipautsons", total_credit_use, 0)
            except Exception as err:
                buyyer_payment_del_sta = True
                seller_payment_del_sta = True
                while(buyyer_payment_del_sta or seller_payment_del_sta):
                    try:
                        buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                        seller_payment_del_sta = del_payment(seller_payment_id)
                    except :
                        pass
                return Response(data={"status": "ERROR1025 Export job fail", "cause": str(err)}, status=503)
            
        else:
            discount = discount_calculate(num_img)
            total_credit_use = (int(num_img)*product_on_job.price)*float(discount)
            user_credit = credit_check(user)
            if (user_credit < total_credit_use):
                return Response(data={"status": "ERROR1032 Export job fail", "cause": "Do not have enough credit point"}, status=503)
            try:
                sub_result = sub_credit(
                    buyyer_payment_id,user, total_credit_use, product_on_job.product_id)
                add_result = add_credit(
                    seller_payment_id,product_on_job.user_id, total_credit_use, product_on_job.product_id)
            except Exception as err:
                buyyer_payment_del_sta = True
                seller_payment_del_sta = True
                while(buyyer_payment_del_sta or seller_payment_del_sta ):
                    try:
                        buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                        seller_payment_del_sta = del_payment(seller_payment_id)
                    except :
                        pass
                return Response(data={"status": "ERROR1074 Export job fail", "cause": str(err)}, status=503)
        
        logger.error('1236')
        logger.error('sub_result : ' +str(sub_result))
        logger.error('add_result : ' +str(add_result))
        if (sub_result != 1  or add_result != 1):
                buyyer_payment_del_sta = True
                seller_payment_del_sta = True
                while(buyyer_payment_del_sta or seller_payment_del_sta):
                    try:
                        buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                        seller_payment_del_sta = del_payment(seller_payment_id)
                    except :
                        pass
                return Response(data={"status": "ERROR1059 Export job fail", "cause": str(add_result)+" and "+str(sub_result)}, status=503)
        logger.error('1247')
        path = "/ipautsons/"+img_path[0]+"/"+img_path[1]+"/"+img_path[2]

        docker_image_name = None
        in_command_file_name = None
        now = datetime.datetime.now()
        time_now = now.strftime("%H")+now.strftime("%M")+now.strftime("%S")
        if (product_on_job != None):
            result_folder_name = img_path[2]+'-'+product_on_job.product_name+'-'+time_now
            result_path = "ipautsons/"+img_path[0]+"/"+img_path[1]+"/"+result_folder_name
            docker_image_name = '"'+"..."+'"'
            in_command_file_name = '"'+"..."+'"'

        else:
            result_folder_name = (img_path[2]+'-'+(request.data['product_id'].replace(" ", "-")))+'-'+time_now
            result_path = "ipautsons/"+img_path[0]+"/"+img_path[1]+"/"+result_folder_name
            match request.data['product_id']:
                case 'Black and White':
                    docker_image_name = "blackwhite"
                    in_command_file_name = '"'+"blackwhite.py"+'"'
                case 'ASCII':
                    docker_image_name = "ascii"
                    in_command_file_name = '"'+"ASCII.py"+'"'
                case 'PixelArt':
                    docker_image_name = "pixel"
                    in_command_file_name = '"'+"pixel.py"+'"'
                case 'Mosaic':
                    docker_image_name = "mosaig"
                    in_command_file_name = '"'+"mosaig.py"+'"'
                    path = "/"+str(request.data['product_value'])
                case other:
                    return Response(data={'status': 'ERROR1077 Create folder fail !!!','cause':str("can not find product")}, status=503)


        logger.error('1281')
        try:
            os.makedirs("/"+result_path)
        except Exception as error:
            print(error)
            return Response(data={'status': 'ERROR1085 Create folder fail !!!','cause':str(error)}, status=503)
        else:
            try:
                folder_data = {
                    'folder_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
                    'user_id': payload['id'],
                    'folder_name': result_folder_name,
                    'path': result_path,
                    'is_hidden': False
                }

                serializer = FolderImageSerializer(data=folder_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as error:
                print(error)
                buyyer_payment_del_sta = True
                seller_payment_del_sta = True
                while(buyyer_payment_del_sta or seller_payment_del_sta ):
                    try:
                        buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                        seller_payment_del_sta = del_payment(seller_payment_id)
                    except :
                            pass
                return Response(data={'status': 'ERROR1101 Create folder fail !!!','cause':str(error)}, status=503)
        
        name_job = '"'+user.first_name+'-'+img_path[2]+'-'+docker_image_name+'-'+str(time_now)+'"'
        path_temp = '"'+path+'"'
        result_path_temp = '"/'+result_path+'"'
        user_id_temp = '"'+str(payload['id'])+'"'
        name_job = name_job.lower()
        logger.error('1309')
#---------------------------------------------------mosaic---------------------------------------------#  
    #masaic = job_id ,user_id ,choose_folder ,image_selected ,result_folder
        if (request.data['product_id'] == 'Mosaic'):
            img_path_temp = '"'+'/ipautsons/'+str(img_sel.path)+'"'
            template = """apiVersion: batch/v1

kind: Job

metadata:

  name: """+str(name_job)+"""

spec:

  template:

    spec:

      containers:

      - name: """+str(name_job)+"""

        image: suteesaraphan27/"""+str(docker_image_name)+"""
        volumeMounts:
            - name: nfs-share
              mountPath: /ipautsons

        command: ["python","""+str(in_command_file_name)+""","""+str(job_id)+""","""+str(user_id_temp)+""","""+str(path_temp)+""","""+str(img_path_temp)+""","""+str(result_path_temp)+"""]

      restartPolicy: Never
      volumes:
      - name: nfs-share
        persistentVolumeClaim: 
          claimName: example"""
            
#---------------------------------------------------pixel---------------------------------------------#            
        elif(request.data['product_id'] == 'PixelArt'):
            #pixel = job_id ,user_id ,base_folder,result_folder,pixel
            pixel_per_bit = str(request.data['product_value']).split(" ")[0]
            pixel_per_bit = '"'+str(pixel_per_bit)+'"'
            template = """apiVersion: batch/v1

kind: Job

metadata:

  name: """+str(name_job)+"""

spec:

  template:

    spec:

      containers:

      - name: """+str(name_job)+"""

        image: suteesaraphan27/"""+str(docker_image_name)+"""
        volumeMounts:
            - name: nfs-share
              mountPath: /ipautsons

        command: ["python","""+str(in_command_file_name)+""","""+str(job_id)+""","""+str(user_id_temp)+""","""+str(path_temp)+""","""+str(result_path_temp)+""","""+str(pixel_per_bit)+"""]

      restartPolicy: Never
      volumes:
      - name: nfs-share
        persistentVolumeClaim: 
          claimName: example"""
        else:
#---------------------------------------------------normal------------------------------------------------#  
            template = """apiVersion: batch/v1

kind: Job

metadata:

  name: """+str(name_job)+"""

spec:

  template:

    spec:

      containers:

      - name: """+str(name_job)+"""

        image: suteesaraphan27/"""+str(docker_image_name)+"""
        volumeMounts:
            - name: nfs-share
              mountPath: /ipautsons

        command: ["python","""+str(in_command_file_name)+""","""+str(job_id)+""","""+str(user_id_temp)+""","""+str(path_temp)+""","""+str(result_path_temp)+"""]

      restartPolicy: Never
      volumes:
      - name: nfs-share
        persistentVolumeClaim: 
          claimName: example"""

        

        try:

            job_data = {
                'job_id': job_id,
                'user_id': user.user_id,
                'path': path,
                'num_img': num_img,
                'img_selected': img_selected,
                'job_status': "0",
                'product_id': product_on_job.product_id,
                'payment_id': buyyer_payment_id
            }
        except Exception as error:
            job_data = {
                'job_id': job_id,
                'user_id': user.user_id,
                'path': path,
                'num_img': num_img,
                'img_selected': img_selected,
                'job_status': "0",
                'payment_id': buyyer_payment_id
            }
        logger.error('1437')
        try:
            serializer = JobSerializer(data=job_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as error:
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                    pass
            return Response(data={"status": "ERROR1175 Export job fail", "cause": str(error)}, status=503)
    
        logger.error('1453')
        try:

            with open('yaml_file/'+job_id+'.yaml', 'w') as yfile:
                yfile.write(template)
                yfile.close()
                yaml_run = YamlRunner(job_id)
                x = yaml_run.run_yaml()
            if (x == 1):
                credit_check(user.user_id)
                return Response(data={"status": "File is made!","credit_left":credit_check(user.user_id)})
            else:
                buyyer_payment_del_sta = True
                seller_payment_del_sta = True
                while(buyyer_payment_del_sta or seller_payment_del_sta ):
                    try:
                        buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                        seller_payment_del_sta = del_payment(seller_payment_id)
                    except :
                        pass
                return Response(data={"status": "ERROR1195 Export job fail", "cause": str(x)}, status=503)
        except Exception as error:
            print(error)
            buyyer_payment_del_sta = True
            seller_payment_del_sta = True
            while(buyyer_payment_del_sta or seller_payment_del_sta ):
                try:
                    buyyer_payment_del_sta = del_payment(buyyer_payment_id)
                    seller_payment_del_sta = del_payment(seller_payment_id)
                except :
                    pass
            return Response(data={"status": "ERROR1206 Export job fail", "cause": str(error)}, status=503)
