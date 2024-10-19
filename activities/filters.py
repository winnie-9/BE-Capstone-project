from django_filters import rest_framework as filters
from .models import Activity

# class ActivityFilter(filters.FilterSet):
#     duration = filters.NumberFilter()
#     duration_gt = filters.NumberFilter(field_name='duration', lookup_expr='gt')
#     duration_lt = filters.NumberFilter(field_name='duration', lookup_expr='lt')
#     calories_burned = filters.NumberFilter()
#     calories_burned_gt = filters.NumberFilter(field_name='calories_burned', lookup_expr='gt')
#     calories_burned_lt = filters.NumberFilter(field_name='calories_burned', lookup_expr='lt')
    

#     class Meta:
#         model = Activity
#         fields = ['duration', 'calories_burned']


class ActivityFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')
    activity_type = filters.ChoiceFilter(choices=Activity.ACTIVITY_TYPES)

    class Meta:
        model = Activity
        fields = ['start_date', 'end_date', 'activity_type']