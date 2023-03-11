from django.urls import path
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView
# )


urlpatterns = [
    path('make_docker_file', views.MakeDockerFile.as_view()),

    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('user', views.UserView.as_view()),
    path('password', views.PasswordView.as_view()),

    path('upload_image', views.ImageView.as_view()),
    path('image/<str:folder_id>', views.ImageView.as_view()),
    path('image/<str:type>/<str:folder_id>', views.ImageView.as_view()),
    path('all_images', views.AllImageView.as_view()),
    path('folder_img', views.FolderView.as_view()),
    path('folder_img/<str:folder_id>', views.FolderView.as_view()),

    path('product', views.ProductView.as_view()),
    path('product/<str:product_id>', views.ProductView.as_view()),
    
    path('payment', views.PaymentView.as_view()),

]
