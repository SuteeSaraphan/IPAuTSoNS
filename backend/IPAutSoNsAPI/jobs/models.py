from django.db import models

class Job(models.Model):
    job_id = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.job_id