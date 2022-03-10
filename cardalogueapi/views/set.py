# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cardalogueapi.models import Set

class SetView(ViewSet):
    def list (self, request):
        """handes GET all"""
        sets = Set.objects.all()
        serializer = SetSerializer(sets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET single"""
        single_set = Set.objects.get(pk=pk)
        serializer = SetSerializer(single_set)
        return Response(serializer.data)

class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('__all__')
