from rest_framework import serializers
from .models import Agent
from django.contrib.auth.models import User


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class AgentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Agent
        fields = ('user', 'description', 'image',
                  'position', 'agent_association')
