from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name','birth_date']

    def __str__(self):
        return self.email
