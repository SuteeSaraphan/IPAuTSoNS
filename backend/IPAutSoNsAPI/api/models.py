from email.policy import default
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

def upload_path_img(instance,filename):
    if(instance.img_folder == "null"):
        return os.path.join("%s" % instance.user_id,"root",filename)
    elif(instance.img_folder != "null"):
        return os.path.join("%s" % instance.user_id,"root","%s" % instance.img_folder,filename)

def upload_path_weight(instance,filename):
    return os.path.join("%s" % instance.user_id,"weight",instance.product_id,filename)

def upload_product_img(instance,filename):
    return os.path.join("%s" % instance.user_id,"weight",instance.product_id,filename)

def upload_path_proof(instance,filename):
    return os.path.join("%s" % instance.user_id,"proof","%s",filename)


class Image_file(models.Model):
    img_id = models.CharField(max_length=100, primary_key=True)
    user_id = models.CharField(max_length=100 , null=False)
    img_type = models.CharField(max_length=20, null=False)
    img_folder = models.CharField(max_length=100, null=False)
    path = models.ImageField(upload_to = upload_path_img, null=False)
    img_size = models.CharField(max_length=20, null=False)
    def __str__(self):
        return self.img_id

class Folder_img(models.Model):
    folder_id = models.CharField(max_length=100, primary_key=True)
    user_id = models.CharField(max_length=100 , null=False)
    folder_name = models.CharField(max_length=100 , null=False)
    path = models.CharField(max_length=200 , null=False)
    is_hidden = models.BooleanField(default = False)
    def __str__(self):
        return self.folder_id

    

class Job(models.Model):
    job_id = models.CharField(max_length=100, primary_key=True) #sent for check and connect
    user_id = models.CharField(max_length=20, null=False) #sent for check and connect
    app_id = models.CharField(max_length=100 ,default="00", null=False)
    path = models.CharField(max_length=200, null=False) #sent for access image folder 
    num_img = models.IntegerField(default=0, null=False) #sent 
    img_selected = models.CharField(max_length=500, null=False) #sent path of image file 
    persent = models.IntegerField(default=0, null=False) #modifi update when process job
    job_status = models.CharField(max_length=100,default=0, null=False) #modifi update when process job
    create_time = models.DateTimeField(editable=False, auto_now_add=True) 

    def __str__(self):
        return self.job_id


class User(AbstractBaseUser):
    user_id = models.CharField(primary_key=True,unique=True,max_length=100)
    password = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, null=False ,unique=True)
    is_vip = models.BooleanField(default=False, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []


    def __str__(self):
        return self.user_id



class Image_app(models.Model):
    app_id = models.CharField(primary_key=True,unique=True,max_length=100)
    app_name = models.CharField(unique=True,max_length=100)
    app_type = models.CharField(max_length=50, null=False)
    parameter = models.IntegerField(default=80)
    model_type = models.CharField(max_length=50, null=True)
    app_path = models.FileField(upload_to=upload_path_weight)

class Product(models.Model):
    product_id = models.CharField(primary_key=True,unique=True,max_length=100)
    user_id = models.CharField(max_length=100, null=False)
    product_name = models.CharField(unique=True,max_length=100, null=False)
    product_type = models.CharField(max_length=100, null=False)
    model = models.CharField(max_length=100, null=False)
    price = models.FloatField(max_length=100, null=False)
    path = models.FileField(upload_to = upload_path_weight, null=False)
    product_img = models.ImageField(upload_to = upload_product_img, null=False)
    last_update = models.DateTimeField(auto_now_add=True, null=False) 

class Login_log(models.Model):
    login_log_id = models.CharField(primary_key=True,unique=True,max_length=100)
    user_id = models.CharField(max_length=100, null=False)
    login_time = models.DateTimeField(editable=False, auto_now_add=True, null=False)

class Payment(models.Model):
    payment_id = models.CharField(primary_key=True,unique=True,max_length=100)
    user_id = models.CharField(max_length=100, null=False)
    product_id = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=50, null=False)
    pay_time = models.DateTimeField(editable=False, auto_now_add=True) 
    # proof = models.ImageField(upload_to = upload_path_proof, null=False) 


