"""Warehouse_Management_System URL Configuration

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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url

# from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_login.urls', namespace='home_and_login')),
    path('users/', include('user_manage.urls', namespace='user_related')),
    path('projects/', include('project_manage.urls', namespace='project_related')),
    path('products/', include('product_manage.urls', namespace='product_related')),
    path('manufacturers/', include('manufacturer_manage.urls', namespace='manufacturer_related')),
    path('purchases/', include('purchase_manage.urls', namespace='purchase_related')),
    path('inbounds/', include('inbound_manage.urls', namespace='godown_related')),
    path('receptions/', include('reception_manage.urls', namespace='receptions_related')),
    path('lendings/', include('lending_manage.urls', namespace='lending_related')),
    path('outbounds/', include('outbound_manage.urls', namespace='outbound_related')),

]
