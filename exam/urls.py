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
from exam_sch.views import roles_create,   user_table_detail,gender_detail
from exam_sch.views import user_table_create,DeptViewSet,SessionViewSet,Programme_LevelViewSet,GenderViewSet
from rest_framework.decorators import api_view
from rest_framework import routers
from exam_sch import views

router = routers.DefaultRouter()
router.register(r'departments', views.DeptViewSet, basename='department')
router.register(r'session', views.SessionViewSet, basename='session')
router.register(r'programe_level', views.Programme_LevelViewSet, basename='programe_level')
router.register(r'gender',views.GenderViewSet,basename= 'gender')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("exam_sch/",include('exam_sch.urls')),
    path('exam_prop/', include(router.urls)),
 
    # path('user_table/create/', user_table_create, name='user-table-create'),
    # path('roles_table/create/',roles_create,name="roles-table-create")
    # Add other URL patterns if needed
]
