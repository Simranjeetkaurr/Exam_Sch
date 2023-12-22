from django.urls import path, include
from rest_framework import routers
from exam_sch.views import user_table_create,subject_list,subject_detail,program_list,program_detail,specialization_search_api
from exam_sch.views import roles_create, create_gender,program_level_detail,program_level_list,roles_detail
from exam_sch.views import user_login,session_list,session_detail,user_table_detail,dept_detail,dept_list,send_email ,password_reset,specialization_detail,specialization_list
from . import views 
from exam_sch.views import semester_detail,semester_list,slot_list,slot_detail,program_search_api,subject_search_api,studentenrollment_list,studentenrollment_detail,studentenrollment_seacrh
from exam_sch.views import electives_search_api,Electives_detail,Electives_list,elec_slot_detail,elec_slot_list,spec_slot_detail,spec_slot_list,studentenrollment_session_seacrh
#from rest_framework.decorators import api_view

router = routers.DefaultRouter()
router.register(r'roles', views.roles_create, basename='roles')
router.register(r'user_table', views.user_table_create, basename='user_table')
router.register(r'departments', views.dept_list, basename='department')
router.register(r'session', views.session_list, basename='session')
router.register(r'programe_level', views.program_level_list, basename='programe_level')
router.register(r'gender',views.create_gender,basename= 'gender')
router.register(r'Subject',views.subject_list, basename = 'Subject')
router.register(r'Program',views.program_list, basename = 'Program')
router.register(r'Semester',views.semester_list, basename = 'semester')
router.register(r'Slot',views.slot_list,basename= 'slot')
router.register(r'StudentEnrollment',views.studentenrollment_list,basename= 'studentenrollment')
router.register(r'Specialization',views.specialization_list,basename= 'Specialization')
router.register(r'Electives',views.Electives_list,basename= 'Electives')
router.register(r'SpecSlot',views.spec_slot_list,basename= 'SpecSlot')
router.register(r'ElecSlot',views.Electives_list,basename= 'ElecSlot')
#urlpatterns = [
#    path('', include(router.urls)),
#    # Add other URL patterns if needed
#]


urlpatterns = [
    # Your existing URL patterns
    path('api/user_table/create', views.user_table_create, name='user_table'),
    path('api/user_table/<int:pk>/', user_table_detail, name='user_table-detail'),
    path('api/roles_create/',views.roles_create,name= 'roles'),
    path('api/roles/<int:pk>/', views.roles_detail, name='roles-detail'),
    path('api/login', views.user_login, name='user-login'),
    path('api/genders_create/', views.create_gender, name='gender-list'),
    path('api/genders/<int:pk>/', views.gender_detail, name='gender-detail'),
    path('api/program_level_list/', views.program_level_list, name='program_level-list'),
    path('api/program_level_detail/<int:pk>/', views.program_level_detail, name='program_level_detail'),
    path('api/program_list/', views.program_list, name='program-list'),
    path('api/program_detail/<int:pk>/', views.program_detail, name='program-detail'),
    path('api/depts_list/', views.dept_list, name='dept-list'),
    path('api/depts_detail/<int:pk>/', views.dept_detail, name='dept-detail'),
    path('api/sessions_list/', views.session_list, name='session-list'),
    path('api/sessions_detail/<int:pk>/', views.session_detail, name='session-detail'),
    path('api/subject_list/', views.subject_list, name='subject-list'),
    path('api/subject_detail/<int:pk>/', views.subject_detail, name='subject-detail'),
    path('api/semester_list/', views.semester_list, name='semester-list'),
    path('api/semester_detail/<int:semester_id>/', views.semester_detail, name='semester-detail'),
    path('api/slots_list/', views.slot_list, name='slot-list'),
    path('api/slots_detail/<int:pk>/', views.slot_detail, name='slot-detail'),
    path('api/program-search/', program_search_api, name='program-search-api'),
    path('api/subject-search/', subject_search_api, name='subject-search-api'),
    path('api/studentenrollment_list/', views.studentenrollment_list, name='studentenrollment-list'),
    path('api/studentenrollment_detail/<int:pk>/', views.studentenrollment_detail, name='studentenrollment-detail'),
    path('api/studentenrollment-search/', studentenrollment_seacrh, name='studentenrollment_seacrh-api'),
    path('api/studentenrollment-session-search/', studentenrollment_session_seacrh, name='studentenrollment_session_search-api'),
    path('api/specialization_list/', views.specialization_list, name='specialization-list'),
    path('api/specialization_detail/<int:pk>/', views.specialization_detail, name='specialization-detail'),
    path('api/specialization-search/', specialization_search_api, name='specialization-search-api'),
    path('api/send-email/', send_email, name='send-email'),
    path('api/electives_list/', views.Electives_list, name='electives-list'),
    path('api/electives_detail/<int:pk>/', views.Electives_detail, name='electives-detail'),
    path('api/electives-search/', electives_search_api, name='electives-search-api'),
    path('api/send-email/', send_email, name='send-email'),
    path('api/password-reset/<str:email>/', password_reset, name='password-reset'),
    path('api/elec_slots_list/', views.elec_slot_list, name='elec-slot-list'),
    path('api/elec_detail/<int:pk>/', views.elec_slot_detail, name='Elec-slot-detail'),
    path('api/spec_slots_list/', views.spec_slot_list, name='spec-slot-list'),
    path('api/spec_detail/<int:pk>/', views.spec_slot_detail, name='spec-slot-detail'),

]
 