from pyexpat import model
from django.db import models


class Job(models.Model):
    job_id = models.CharField(max_length=100, primary_key=True)
    user_id = models.CharField(max_length=100)
    app_id = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    num_img = models.IntegerField(default=0)
    img_selected = models.CharField(max_length=500)
    persent = models.IntegerField(default=0)
    job_status = models.CharField(max_length=100)
    create_time = models.DateTimeField(editable=False, auto_now_add=True)

    def __str__(self):
        return self.job_id
