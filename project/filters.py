import django_filters
from CrowdFunding.project.models import Project

class ProjectFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name')
    tag = django_filters.CharFilter(field_name='tags__name')
    min_goal = django_filters.NumberFilter(field_name='goal', lookup_expr='gte')
    max_goal = django_filters.NumberFilter(field_name='goal', lookup_expr='lte')

    class Meta:
        model = Project
        fields = ['category', 'tag', 'status']