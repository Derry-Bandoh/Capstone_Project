from django.db import models
from django.conf import settings


##  Choices for priority field
class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        CRITICAL = 4,'Critical'


## Choices for status field
class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETED = 'C', 'Completed'

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)


    class Meta:
        ordering = ['due_date', '-priority']
        db_table = 'tasks'

    def __str__(self):
        return f'{self.user.email} - {self.title[:50]} ({self.get_status_display()})'