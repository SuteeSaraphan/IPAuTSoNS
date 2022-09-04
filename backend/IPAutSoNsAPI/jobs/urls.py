from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListJob.as_view()),
    path('<slug:pk>/', views.DetailJob.as_view()),
    path('lastest', views.LastestJob.as_view()),
    path('do_job', views.make_yaml),
]
