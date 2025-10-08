from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Ensuring the password is not returned after registration and requires confirmation
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = CustomUser
        # Explicitly including the standard fields plus the profile picture
        fields = ['username', 'email', 'password', 'password2', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'email': {'required': True},
        }

    def validate(self, data):
        """Check that the two password fields match."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """Create and return a new CustomUser instance."""
        # Removing the password confirmation field before creating the user
        validated_data.pop('password2')
        
        # Creating the user using the custom manager's create_user method (inherited from AbstractUser)
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            profile_picture=validated_data.get('profile_picture')
        )
        return user