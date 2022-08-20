from django.shortcuts import render
from rest_framework import generics
from .models import Job
from .serializers import JobSerializer

class ListJob(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
class DetailJob(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer 

