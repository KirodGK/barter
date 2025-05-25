from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AnnouncementViews

app_name = 'api'

router = DefaultRouter()
router.register(r'announcement', AnnouncementViews, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
]