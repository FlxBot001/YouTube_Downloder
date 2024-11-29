from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DownloadViewSet

router = DefaultRouter()
router.register(r'download', DownloadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]