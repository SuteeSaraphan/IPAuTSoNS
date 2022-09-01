import yaml
from time import sleep
from django.shortcuts import render
from rest_framework import generics
from .models import Job
from .serializers import JobSerializer
from django.http import HttpResponse


class ListJob(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-create_time')
    serializer_class = JobSerializer
    
    
class DetailJob(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer 


class LastestJob(generics.ListCreateAPIView):
    queryset = Job.objects.all().filter(job_status=0).order_by('-create_time')[:1]
    serializer_class = JobSerializer


def make_yaml(request):
    sleep(1)
    print("going to make file")
    lastest_job = Job.objects.all().filter(job_status=0).order_by('create_time')[:1]
    print(lastest_job[0].job_id)
    lastest_job_2yaml = [
        {"job_id": lastest_job[0].job_id,
        "user_id": lastest_job[0].user_id, 
        "path": lastest_job[0].path,
        "num_img": lastest_job[0].num_img,
        "persent": lastest_job[0].persent,
        "job_status": lastest_job[0].job_status,
        "create_time": lastest_job[0].create_time}]
    with open('yaml_file/'+lastest_job[0].job_id+'.yaml', 'w') as f:
        yaml.dump(lastest_job_2yaml, f)


    lastest_job = Job.objects.get(job_id=lastest_job[0].job_id)
    lastest_job.job_status=1
    lastest_job.save()





    return HttpResponse("""<html><script>    windwow.location.replace('/');   </script></html>""")




