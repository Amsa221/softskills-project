from django.contrib import admin
from .models import DailyStat

@admin.register(DailyStat)
class DailyStatAdmin(admin.ModelAdmin):
    list_display = ("date", "total_revenue", "total_transactions")
    ordering = ("-date",)