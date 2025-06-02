from rest_framework import viewsets, permissions, filters
from .models import Donation
from .serializers import DonationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['project', 'amount', 'created_at']
    ordering_fields = ['amount', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProjectTotalDonationsView(APIView):
    def get(self, request, pk):
        total = Donation.objects.filter(project_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"project_id": pk, "total_donated": total})
