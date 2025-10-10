import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    # Customized filtering for Due Date to allow range queries
    due_date__gt = django_filters.DateFilter(field_name='due_date', lookup_expr='gt')
    due_date__lt = django_filters.DateFilter(field_name='due_date', lookup_expr='lt')

    class Meta:
        model = Task
        fields = ['status', 'priority']