"""
URL configuration for exam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from rest_framework.decorators import api_view
from rest_framework import routers
from exam_sch import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("exam_sch/",include('exam_sch.urls')),
 
    # path('user_table/create/', user_table_create, name='user-table-create'),
    # path('roles_table/create/',roles_create,name="roles-table-create")
    # Add other URL patterns if needed
]
