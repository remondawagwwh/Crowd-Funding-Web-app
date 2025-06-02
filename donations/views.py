from datetime import timezone
from rest_framework import generics, permissions
from .models import Donation
from .serializers import DonationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from project.models import Project
from django.db.models import Sum

from donations import serializers

class CreateDonationView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if project.is_cancelled or timezone.now() > project.end_time:
            raise serializers.ValidationError("Project is not available for donation.")
        serializer.save(user=self.request.user)


class ProjectTotalDonationsView(APIView):
    def get(self, request, pk):
        total = Donation.objects.filter(project_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"project_id": pk, "total_donated": total})
