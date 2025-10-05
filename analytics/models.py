from django.db import models

class DailyStat(models.Model):
    date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_transactions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.total_revenue} CFA"
