import django_filters
from .models import Donation

class DonationFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Donation
        fields = {
            'user': ['exact'],
            'project': ['exact'],
        }
