# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
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

    @action(methods=['put'], detail=True)
    def admin(self, request, pk):
        """Put request to is_staff"""

        user = User.objects.get(pk=pk)
        user.is_staff = True
        user.save()

        return Response({'message': 'User is now an admin'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def collector(self, request, pk):
        """Put request to is_staff"""

        user = User.objects.get(pk=pk)
        admin_list = User.objects.filter(is_staff=True, is_active=True)
        serialized = UserSerializer(admin_list, many=True)

        if len(serialized.data) <= 1 and user.is_staff is True:
            return Response({'message': 'this is the only active admin remaining'},
                            status=status.HTTP_409_CONFLICT)
        else:
            user.is_staff = False
            user.save()
            return Response({'message': 'User is now an author'}, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
    