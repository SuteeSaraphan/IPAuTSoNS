from django.urls import path
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView
# )


urlpatterns = [
    path('jobs', views.ListJob.as_view()),
    path('users', views.ListUser.as_view()),

    path('make_docker_file', views.MakeDockerFile.as_view()),

    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('user', views.UserView.as_view()),
    path('password', views.PasswordView.as_view()),

    path('image', views.ImageView.as_view()),

   

]
