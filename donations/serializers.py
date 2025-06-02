from rest_framework import serializers
from .models import Donation
from django.utils import timezone

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'user', 'project', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def validate(self, attrs):
        project = attrs.get('project')
        if project.is_cancelled:
            raise serializers.ValidationError("Cannot donate to a cancelled project.")
        if timezone.now() > project.end_time:
            raise serializers.ValidationError("Cannot donate to an expired project.")
        return attrs
