from rest_framework import serializers
from users_api import models
class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)

class UsersSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserModel
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserModel.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


# class ProfileFeedItemSerializer(serializers.ModelSerializer):
#     """Serializes profile feed items"""
#
#     class Meta:
#         model = models.ProfileFeedItem
#         fields = ('id', 'users_api', 'status_text', 'created_on')
#         extra_kwargs = {'user_profile': {'read_only': True}}
