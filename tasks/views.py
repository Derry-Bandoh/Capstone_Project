from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer, TaskCompletionSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing, creating, editing, and deleting Task instances (CRUD).
    It ensures users only see and manage their own tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Enables filtering based on TaskFilter
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    # Enables searching and ordering
    ordering_fields = ['priority', 'due_date', 'created_at']
    ordering = ['-due_date']

    #Ensures tasks are user-specific
    def get_queryset(self):
        """Filters the queryset to only show tasks belonging to the currently logged-in user."""
        return Task.objects.filter(user=self.request.user)

    #Assigns Task to User
    def perform_create(self, serializer):
        """Automatically sets the 'user' field to the current user upon creation."""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        # Check if task is completed and prevent editing
        if self.get_object().status == 'C' and self.get_object().status == serializer.validated_data.get('status', 'C'):
            return Response(
                {"error": "Completed tasks cannot be edited. Mark as pending first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_completion(self, request, pk=None):
        """
        Mark a task as complete or incomplete
        POST /tasks/{id}/toggle_completion/
        
        Expected payload:
        {
            "status": "C"  # for completed or "P" for pending
        }
        """
        task = self.get_object()
        
        # Check if user owns this task
        if task.user != request.user:
            return Response(
                {"error": "You can only update your own tasks."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TaskCompletionSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

