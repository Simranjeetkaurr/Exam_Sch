from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet

# Create a router for automatic URL routing
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    # Include the router URLs for the 'Department' model
    path('', include(router.urls)),
]

# The department-related URLs include:

# List departments (GET): /exm_sch/departments/
# Create a department (POST): /exm_sch/departments/
# Retrieve a department (GET): /exm_sch/departments/<pk>/
# Update a department (PUT, PATCH): /exm_sch/departments/<pk>/
# Delete a department (DELETE): /exm_sch/departments/<pk>/