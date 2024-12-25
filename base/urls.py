from django.urls import path, include
from .views import authView, home
from django.contrib.auth import views as auth_views
from . import views

app_name = 'base'  # Ensure the namespace is declared
urlpatterns = [
  path('', views.home, name='home'),  # Home page
  path("signup/", authView, name="authView"),
  path("accounts/", include("django.contrib.auth.urls")),
  path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('add-car/', views.add_car, name='add_car'),
  path('car/<int:car_id>/page_one/', views.car_page_one, name='car_page_one'),
  path('car/<int:car_id>/page_two/', views.car_page_two, name='car_page_two'),
  path('car/<int:car_id>/page_three/', views.car_page_three, name='car_page_three'),
  path('upload-unknown-image/', views.upload_unknown_image, name='upload_unknown_image'),
  path('car/<int:car_id>/images/', views.page_two, name='car_images'),
  path('car/<int:car_id>/empty/', views.car_page_empty, name='car_page_empty'),  # New empty page
  path('api/get-user-images/<int:user_id>/<int:car_id>/', views.get_user_images, name='get_user_images'),
  path('api/get-media-image/<str:name>/', views.get_media_image, name='get_media_image'),
  path('car/<int:car_id>/images/', views.page_two, name='car_images'),
]