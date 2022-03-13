# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
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

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            user = request.auth.user
            serializer = CreateCollectionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk):
        """Handle PUT requests for a collection

        Returns:
            Response -- Empty body with 204 status code
        """
        collection = Collection.objects.get(pk=pk)
        serializer = CreateCollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for collection
        Returns:
            Response -- empty body with 204 status code
        """
        try:
            collection = Collection.objects.get(pk=pk)
            collection.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('__all__')
        depth = 2

class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name', 'date', 'card')
