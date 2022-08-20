from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListJob.as_view()),
    path('<int:pk>/', views.DetailJob.as_view()),
]