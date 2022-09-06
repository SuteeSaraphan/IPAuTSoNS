from django.urls import path
from . import views

urlpatterns = [
    path('jobs', views.ListJob.as_view()),
    path('users', views.ListUser.as_view()),
    #path('<slug:pk>/', views.DetailJob.as_view()),
    path('lastest', views.LastestJob.as_view()),
    path('do_job', views.make_yaml),
    path('login/<str:email>/<str:password>/', views.login_page)

]
