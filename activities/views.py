from rest_framework import viewsets, permissions, views, generics
from .models import Activity 
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ActivityFilter
from rest_framework.response import Response
from django.db.models.functions import TruncWeek, TruncMonth
from .serializers import ActivitySerializer, ActivityHistorySerializer
from django.db.models import Sum, Count
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .serializers import ActivityMetricsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    authentication_classes = [JWTAuthentication]

    

#class ActivityViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]


    # def post(self, request, *args, **kwargs):
    #     # Create a new activity metric
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED) 



    filterset_class = ActivityFilter
    search_fields = ['activity_type']


    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, *args, **kwargs):
    #     request.data['user'] = request.user.id
    #     return super().update(request, *args, **kwargs)
    

    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


    # def get_queryset(self):
    #     queryset = self.queryset
    #     sort_by = self.request.GET.get('sort_by')
    #     if sort_by:
    #         if sort_by == 'date':
    #             queryset = queryset.order_by('date')
    #         elif sort_by == 'duration':
    #             queryset = queryset.order_by('duration')
    #         elif sort_by == 'calories_burned':
    #             queryset = queryset.order_by('calories_burned')
    #     return queryset



# class ActivityHistoryView(views.APIView):
#     queryset = Activity.objects.all()
#     serializer_class = ActivitySerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = ActivityFilter
#     search_fields = ['activity_type']


class ActivityHistoryView(generics.ListAPIView):
    serializer_class = ActivityHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ActivityFilter

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).order_by('-date')


# class ActivitySummaryView(views.APIView):
#     def get(self, request):
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')

#         queryset = Activity.objects.filter(user=request.user)
#         if start_date:
#             queryset = queryset.filter(date__gte=start_date)
#         if end_date:
#             queryset = queryset.filter(date__lte=end_date)

#         summary = queryset.aggregate(
#             total_duration=Sum('duration'),
#             total_distance=Sum('distance'),
#             total_calories_burned=Sum('calories_burned')
#         )

#         serializer = ActivitySummarySerializer(summary)
#         return Response(serializer.data)
    


# class ActivityTrendView(views.APIView):
#     def get(self, request):
#         period = self.request.query_params.get('period', 'week')
#         trunc_func = TruncWeek if period == 'week' else TruncMonth

#         trends = Activity.objects.filter(user=request.user) \
#             .annotate(period=trunc_func('date')) \
#             .values('period') \
#             .annotate(
#                 total_duration=Sum('duration'),
#                 total_distance=Sum('distance'),
#                 total_calories_burned=Sum('calories_burned')
#             ) \
#             .order_by('period')

#         serializer = ActivityTrendSerializer(trends, many=True)
#         return Response(serializer.data)



class ActivityMetricsView(generics.RetrieveAPIView):
    serializer_class = ActivityMetricsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get query parameters
        period = self.request.query_params.get('period', 'week')
        end_date = timezone.now().date()
        
        if period == 'month':
            start_date = end_date - relativedelta(months=1)
        else:  # default to week
            start_date = end_date - relativedelta(weeks=1)

        # Calculate metrics
        metrics = Activity.objects.filter(
            user=self.request.user,
            date__range=[start_date, end_date]
        ).aggregate(
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_calories_burned=Sum('calories_burned'),
            activity_count=Count('id')
        )


        metrics['start_date'] = start_date
        metrics['end_date'] = end_date

# Format the duration
        total_seconds = metrics['total_duration']
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        metrics['total_duration'] = f"{hours} hours, {minutes} minutes, {seconds} seconds"

        return metrics
    
    