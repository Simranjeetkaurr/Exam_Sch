# from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.urls import path, include
from .views import DepartmentViewSet, SessionViewSet

router = routers.DefaultRouter()
# router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'sessions', SessionViewSet)

# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
]