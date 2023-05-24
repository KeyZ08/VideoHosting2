"""VideoHosting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from . import views
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),

    path('account/', account, name='account'),
    path('account/avatar_upload/', avatar_upload, name='avatar_upload'),
    path('account/avatar_reset/', avatar_reset, name='avatar_upload'),
    path('account/video_upload/', video_upload, name='video_upload'),
    path('account/history/', views.video_history, name='video_history'),
    path('accounts/<str:username>/', account),


    path('videos/<str:id_video>/change/', video_change, name='video_change'),
    path('videos/<str:id_video>/delete/', video_delete, name='video_delete'),

    path('videos/<str:id_video>/like/', views.like, name='like'),
    path('videos/<str:id_video>/dislike/', views.dislike, name='dislike'),

    path('videos/<str:id_video>/add-comment/', views.add_comment, name='add-comment'),
    path('videos/<str:id_video>/delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
