# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action

from django.contrib.auth.models import User

class UserView(ViewSet):
    def list (self, request):
        """handes GET all"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET single"""
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False)
    def current(self, request):
        """Only get actors back that are currently active on a book"""

        user=request.auth.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
    