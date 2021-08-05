"""View module for handling requests about gamers"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Gamer
from django.contrib.auth.models import User


class GamerView(ViewSet):
    """Level up Gamers"""

    def list(self, request):
        """Handle GET requests to gamers resource
        
        Returns JSON serialized list of gamers
        """
        gamers = Gamer.objects.all()
        serializer = GamerSerializer(
            gamers, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['id', 'user']
