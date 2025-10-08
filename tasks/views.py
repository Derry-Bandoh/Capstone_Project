from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing, creating, editing, and deleting Task instances (CRUD).
    It ensures users only see and manage their own tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    #Ensures tasks are user-specific 
    def get_queryset(self):
        """Filters the queryset to only show tasks belonging to the currently logged-in user."""
        return Task.objects.filter(user=self.request.user)

    #Assigns Task to User 
    def perform_create(self, serializer):
        """Automatically sets the 'user' field to the current user upon creation."""
        serializer.save(user=self.request.user)
