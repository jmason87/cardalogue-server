# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cardalogueapi.models import Collection

class CollectionView(ViewSet):
    def list (self, request):
        """handes GET all"""
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET single"""
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('__all__')
        depth = 1
