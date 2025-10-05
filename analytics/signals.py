from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Payment
from .models import DailyStat
from django.utils.timezone import now

@receiver(post_save, sender=Payment)
def update_stats(sender, instance, created, **kwargs):
    if instance.status == "completed":
        today = instance.created_at.date()
        stat, _ = DailyStat.objects.get_or_create(date=today)
        stat.total_revenue += instance.amount
        stat.total_transactions += 1
        stat.save()
