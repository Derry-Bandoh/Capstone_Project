from rest_framework import serializers
from django.utils import timezone
from .models import Task 


##Allowing any case of the letter to saved to the model 
class UppercaseField(serializers.CharField):
    def to_internal_value(self, data):
        return super().to_internal_value(data).upper()

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model, handles conversion to/from JSON.
    It includes read-only fields for displaying the full priority/status labels.
    """
    # These fields retrieve the human-readable labels like 'Low', 'Pending'
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    
    username = serializers.CharField(source='user.username', read_only=True)
    status = UppercaseField(required = False)
    
    
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
            'completed_at',   
            'created_at', 
            'due_date', 
            'username',
        )
        # This prevent users from modifying the user field directly
        read_only_fields = ('username', 'created_at','completed_at')
        
        extra_kwargs = {
            'description':{'required': True},
            'priority': {'required':True},
            # 'status': {'required': True},
            'due_date': {'required': True},
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make status read-only on creation, writable on update
        if not self.instance:  # If creating
            self.fields['status'].read_only = True

    def validate(self,data):
        """
        Validate that completed tasks cannot be editted unless reverted to pending
        """
        if self.instance and self.instance.status == 'C':
            if 'status' in data and data['status'] == 'P':
                return data
            elif 'status' not in data:
                raise serializers.ValidationError(
                    "Completed tasks cannot be edited. Revert to pending first"
                )
            else:
                raise serializers.ValidationError(
                    "Completed tasks cannot be edited. Revert to pending first"
                )
        return data 

class TaskCompletionSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for marking tasks as complete or incomplete
    """
    status = UppercaseField()
    
    class Meta:
        model = Task
        fields = ['status', 'completed_at']
        read_only_fields = ['completed_at']
    
    def validate_status(self, value):
        if value not in ['P', 'C']:
            raise serializers.ValidationError(
                "Status must be either 'P' (Pending) or 'C' (Completed)"
            )
        return value
    
    def update(self, instance, validated_data):
        """
        Update task status and set completed_at timestamp
        """
        new_status = validated_data.get('status', instance.status)
        
        # Set completed_at timestamp when marking as completed
        if new_status == 'C':
            instance.completed_at = timezone.now()
        # Clear timestamp when reverting to pending
        elif new_status == 'P':
            instance.completed_at = None
        
        instance.status = new_status
        instance.save()
        return instance

    
    
