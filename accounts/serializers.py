from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Ensuring the password is not returned after registration and requires confirmation
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(read_only=True)
    
    class Meta:
        model = CustomUser
        # Explicitly including the standard fields plus the profile picture
        fields = ['username','first_name','last_name','birth_date', 'email', 'password', 'password2', 'profile_picture','token']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'first_name':{'required': True},
            'last_name': {'required': True},
            'birth_date': {'required': True},
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
            first_name=validated_data['first_name'],
            last_name= validated_data['last_name'],
            birth_date= validated_data['birth_date'],
            profile_picture=validated_data.get('profile_picture')
        )
        Token.objects.create(user=user)
        return user