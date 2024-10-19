from rest_framework import serializers
from .models import Activity, ActivityType
from datetime import timedelta

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ['id', 'name']

class ActivitySerializer(serializers.ModelSerializer):
    activity_type = serializers.ChoiceField(choices=Activity.ACTIVITY_TYPES)
    
    class Meta:
        model = Activity 
        fields = ['id', 'user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date', 'history']
        write_only_fields = ['users', 'history']
        # extra_kwargs = {'user': {'write_only': True}, 'history': {'write_only': True}} 


    def validate(self, data):
        """
        Check that the activity type, duration, and date are provided.
        """
        if not data.get('activity_type'):
            raise serializers.ValidationError("Activity type is required.")
        if not data.get('duration'):
            raise serializers.ValidationError("Duration is required.")
        if not data.get('date'):
            raise serializers.ValidationError("Date is required.")
        return data
    
        

class ActivityHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'activity_type', 'duration', 'calories_burned', 'date']


# Activity Metrics
# class ActivitySummarySerializer(serializers.Serializer):
#     total_duration = serializers.IntegerField()
#     total_distance = serializers.FloatField()
#     total_calories_burned = serializers.IntegerField()

# class ActivityTrendSerializer(serializers.Serializer):
#     period = serializers.CharField()
#     total_duration = serializers.IntegerField()
#     total_distance = serializers.FloatField()
#     total_calories_burned = serializers.IntegerField()
class CustomDurationField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, str):
            return value  # If it's already a string, return as is
        delta = timedelta(seconds=value)
        total_seconds = delta.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours} hours, {minutes} minutes, {seconds} seconds"

    def to_internal_value(self, data):
        if isinstance(data, str):
            parts = data.split(',')
            hours = int(parts[0].split(' ')[0])
            minutes = int(parts[1].split(' ')[0])
            seconds = int(parts[2].split(' ')[0])
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
        elif isinstance(data, int):
            return data
        else:
            raise serializers.ValidationError("Invalid duration format")

class ActivityMetricsSerializer(serializers.Serializer):
    total_duration = CustomDurationField()
    total_distance = serializers.FloatField()
    total_calories_burned = serializers.IntegerField()
    activity_count = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()