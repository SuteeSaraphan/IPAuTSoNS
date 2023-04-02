from django.urls import path
from . import views

urlpatterns = [
    path('make_docker_file', views.MakeDockerFile.as_view()),
    path('version',views.VersionCheck.as_view()),

    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('user', views.UserView.as_view()),
    path('password', views.PasswordView.as_view()),

    path('image', views.ImageView.as_view()),
    path('image/<str:folder_id>', views.ImageView.as_view()),
    path('image/<str:type>/<str:folder_id>', views.ImageView.as_view()),
    path('all_images', views.AllImageView.as_view()),
    path('folder_img', views.FolderView.as_view()),
    path('folder_img/<str:folder_id>', views.FolderView.as_view()),

    path('product', views.ProductView.as_view()),
    path('product/<str:type>/<str:key>', views.ProductView.as_view()),

    path('payment', views.PaymentView.as_view()),

    path('product_history/<str:product_id>/<str:type>', views.ProductHistoryView.as_view()),

    path('preview', views.PreviewView.as_view())

]
