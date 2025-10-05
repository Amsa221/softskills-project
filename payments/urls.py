from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet
from . import views
from django.urls import path

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = router.urls

urlpatterns = [
    path('', views.payments_list, name='payment_list'),
]