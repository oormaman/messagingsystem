from rest_framework import serializers
from users_api import models

# class HelloSerializer(serializers.Serializer):
#     """Serializes a name field for testing out APIView"""
#     message = serializers.CharField(max_length=10)

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

class MessageItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.MessageItem
        fields = ('id', 'sender_id','recipient_id', 'subject','message', 'created_on','recipient_of_the_message_read_it')
        extra_kwargs = {'sender': {'read_only': True}}
