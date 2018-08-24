"""Hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import urls
from django.urls import path,include
from Account.views import signup,signin,error,esignin
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('error/',error,name='error'),
    path('esignin/',esignin,name='esignin'),
    path('join/',signup,name='join'),
    path('login/',signin,name='signin'),
    path('', include('board.urls', namespace='board')),
    path('logout/',auth_views.logout,{'next_page':'/'},name='logout'),
]
