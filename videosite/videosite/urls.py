"""videosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path, re_path, reverse
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    #index page
    #path('',views.cam_list, name='index'),
    path('',views.cam_preview, name='index'),

    # cam preview
    path('preview/',views.cam_preview, name='cam_preview'),

    # cam stream
    path('stream/',views.CamStream, name='cam_stream'),


    # cam list
    path('cams/',views.cam_list, name='cam_list'),

    # cam forms
    path('cam/new/', views.CreateCam.as_view(), name='create_cam'),
    path('cam/modify/<int:pk>/', views.ModifyCam.as_view(), name='modify_cam'),
    path('cam/details/<int:pk>/', views.CamDetails.as_view(), name='cam_details'),
    path('cam/delete/<int:pk>/', views.DeleteCam.as_view(), name='delete_cam'),

    # admin
    # path('admin/', admin.site.urls),
]
