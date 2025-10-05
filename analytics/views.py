from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DailyStat
from .serializers import DailyStatSerializer
from django.shortcuts import render

class DailyStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyStat.objects.all().order_by('-date')
    serializer_class = DailyStatSerializer
    permission_classes = [IsAuthenticated]

def analytics_home(request):
    return render(request, 'analytics/index.html')