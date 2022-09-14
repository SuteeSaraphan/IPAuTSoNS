from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Job(models.Model):
    job_id = models.CharField(max_length=100, primary_key=True)
    user_id = models.CharField(max_length=100)
    app_id = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    num_img = models.IntegerField(default=0)
    img_selected = models.CharField(max_length=500)
    persent = models.IntegerField(default=0)
    job_status = models.CharField(max_length=100,default=0)
    create_time = models.DateTimeField(editable=False, auto_now_add=True)

    def __str__(self):

        
        return self.job_id


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=100, null=False ,unique=True)
    password = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, primary_key=True, null=False ,unique=True)
    is_vip = models.BooleanField(default=False, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []


    def __str__(self):
        return self.user_id
