from django.urls import path
from .views import ActivityViewSet, ActivityHistoryView, ActivityMetricsView


urlpatterns = [
    path('activities/', ActivityViewSet.as_view({'get': 'list'}), name='activities_list'),
    path('activities/create/', ActivityViewSet.as_view({'post': 'create'}), name='activities_create'),
    path('activities/<int:pk>/', ActivityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='activities_detail'),
    path('activities/history/', ActivityHistoryView.as_view(), name='activities_history'),

    # path('activities/summary/', ActivitySummaryView.as_view(), name='activity-summary'),
    # path('activities/trends/', ActivityTrendView.as_view(), name='activity-trends'),

    path('activities/metrics/', ActivityMetricsView.as_view(), name='activity-metrics'),

]
