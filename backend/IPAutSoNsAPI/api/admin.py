import imghdr
from django.contrib import admin
from .models import Folder_img, Job,User,Image

# Register your models here.
admin.site.register(Job)
admin.site.register(User)
admin.site.register(Image)
admin.site.register(Folder_img)