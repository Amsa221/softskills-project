from rest_framework.routers import DefaultRouter
from .views import DailyStatViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'analytics', DailyStatViewSet, basename='analytics')

urlpatterns = router.urls

urlpatterns = [
    path('', views.analytics_home, name='analytics_home'),
]
