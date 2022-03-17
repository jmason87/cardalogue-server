# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from cardalogueapi.models import CardCollection

class CardCollectionView(ViewSet):
    def list (self, request):
        """handes GET all"""
        card_coll = CardCollection.objects.all()
        serializer = CardCollectionSerializer(card_coll, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET single"""
        card_coll = CardCollection.objects.get(pk=pk)
        serializer = CardCollectionSerializer(card_coll)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            serializer = CreateCardCollectionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a category

        Returns:
            Response -- Empty body with 204 status code
        """
        card_coll = CardCollection.objects.get(pk=pk)
        serializer = CreateCardCollectionSerializer(card_coll, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        """Handle DELETE requests for category
        Returns:
            Response -- empty body with 204 status code
        """
        try:
            card_coll = CardCollection.objects.get(pk=pk)
            card_coll.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except CardCollection.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class CardCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardCollection
        fields = ('__all__')


class CreateCardCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardCollection
        fields = ('id', 'card', 'collection')
