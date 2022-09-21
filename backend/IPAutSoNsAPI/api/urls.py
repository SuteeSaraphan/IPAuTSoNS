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
    #path('<slug:pk>/', views.DetailJob.as_view()),
    path('lastest', views.LastestJob.as_view()),
    path('do_job', views.make_yaml),


    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),



    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('user', views.UserView.as_view()),
    path('password', views.PasswordView.as_view()),
   

]
