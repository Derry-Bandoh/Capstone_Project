from rest_framework import serializers
from .models import Task 

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model, handles conversion to/from JSON.
    It includes read-only fields for displaying the full priority/status labels.
    """
    # These fields retrieve the human-readable labels like 'Low', 'Pending'
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Task
        fields = (
            'id', 
            'title', 
            'description', 
            'priority', 
            'priority_display', 
            'status', 
            'status_display',   
            'created_at', 
            'due_date', 
            # 'user',
            'username',
        )
        # This prevent users from modifying the user field directly
        read_only_fields = ('username', 'created_at',)