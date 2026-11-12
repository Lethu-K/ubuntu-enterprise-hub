from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessViewSet, home

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),
]