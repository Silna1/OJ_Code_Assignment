from django.urls import path
from . import views
from django.urls import path, include
from rest_framework import routers
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as rest_framework_views
from .views import PhotoItemViews
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
   path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('api-overview/', PhotoItemViews.as_view(), name="api-overview"),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^api-token-auth/', obtain_jwt_token),
]
