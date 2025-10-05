from rest_framework import serializers
from .models import DailyStat

class DailyStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStat
        fields = "__all__"