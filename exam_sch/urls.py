from django.urls import path, include
from rest_framework import routers
from exam_sch.views import user_table_create
from exam_sch.views import roles_create, create_gender,program_level_detail,program_level_list,roles_detail
from exam_sch.views import user_login,DeptViewSet,SessionViewSet,user_table_detail
from . import views
from rest_framework.decorators import api_view

router = routers.DefaultRouter()
router.register(r'roles', views.roles_create, basename='roles')
router.register(r'user_table', views.user_table_create, basename='user_table')
router.register(r'departments', views.DeptViewSet, basename='department')
router.register(r'session', views.SessionViewSet, basename='session')
router.register(r'programe_level', views.Programme_LevelViewSet, basename='programe_level')
router.register(r'gender',views.GenderViewSet,basename= 'gender')

#urlpatterns = [
#    path('', include(router.urls)),
#    # Add other URL patterns if needed
#]


urlpatterns = [
    # Your existing URL patterns
    path('api/user_table/create', views.user_table_create, name='user_table'),
    path('api/user_table/<int:pk>/', user_table_detail, name='user_table-detail'),
    path('api/roles_create',views.roles_create,name= 'roles'),
    path('api/roles/<int:pk>/', views.roles_detail, name='roles-detail'),
    path('api/login', views.user_login, name='user-login'),
    path('api/user_table/<int:pk>/', views.user_table_detail, name='user_table-detail'),
    path('api/genders/', views.create_gender, name='gender-list'),
    path('api/genders/<int:pk>/', views.gender_detail, name='gender-detail'),
    path('api/program_level_list/', views.program_level_list, name='program_level-list'),
    path('api/program_level_detail/<int:pk>/', views.program_level_detail, name='program_level_detail'),
    path('program_types/', views.program_type_list, name='program-type-list'),
    path('program_types/<int:pk>/', views.program_type_detail, name='program-type-detail'),

]


 