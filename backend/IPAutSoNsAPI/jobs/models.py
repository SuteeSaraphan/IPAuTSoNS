from pyexpat import model
from django.db import models

class Job(models.Model):
    job_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    num_img = models.IntegerField(default=0)
    persent = models.IntegerField(default=0)
    job_status = models.IntegerField(default=0)
    
    def __str__(self):
        return self.job_id