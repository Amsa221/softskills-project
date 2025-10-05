from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # On lie automatiquement le paiement à l'utilisateur connecté
        serializer.save(user=self.request.user)
        
from django.shortcuts import render

def payments_list(request):
    payments = [
        {"id": 1, "user": "Fatou", "amount": 15000, "status": "Succès", "date": "2025-08-31"},
        {"id": 2, "user": "Ousmane", "amount": 20000, "status": "Échoué", "date": "2025-08-30"},
        {"id": 3, "user": "Aïcha", "amount": 12000, "status": "Succès", "date": "2025-08-29"},
    ]
    return render(request, "payments/payments.html", {"payments": payments})

