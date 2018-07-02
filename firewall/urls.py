from django.urls import path, include
from rest_framework.routers import DefaultRouter

from firewall import views

router = DefaultRouter()
router.register('', views.FirewallDeviceView)

urlpatterns = [
    path('', include(router.urls)),
]
