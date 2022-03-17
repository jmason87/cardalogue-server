# from django.http import HttpResponseServerError
import stat
from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.files.base import ContentFile
import uuid
import base64
from django.db.models import Q
from cardalogueapi.models import Card

class CardView(ViewSet):
    def list (self, request):
        """handes GET all"""
        
        search_text = self.request.query_params.get('q', None)
        
        cards = Card.objects.all()
        
        if search_text is not None:
            cards=Card.objects.filter(
                Q(first_name__contains=search_text) |
                Q(last_name__contains=search_text)
            )
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET single"""
        card = Card.objects.get(pk=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            serializer = CreateCardSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            imgdata = ContentFile(base64.b64decode(imgstr), name=f'{request.data["first_name"]}-{uuid.uuid4()}.{ext}')
            card = serializer.save(image = imgdata)
            card.tag.set(request.data["tag"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a card

        Returns:
            Response -- Empty body with 204 status code
        """
        card = Card.objects.get(pk=pk)
        serializer = CreateCardSerializer(card, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    def destroy(self, request, pk):
        """Handle DELETE requests for card
        Returns:
            Response -- empty body with 204 status code
        """
        try:
            card = Card.objects.get(pk=pk)
            card.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Card.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['put'], detail=True)
    def approve(self, request, pk):
        card = Card.objects.get(pk=pk)
        card.is_approved = True
        card.save()
        return Response({'message': 'Card is approved'}, status=status.HTTP_204_NO_CONTENT)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('__all__')
        depth = 1

class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'first_name', 'last_name', 'card_number',
                  'card_category', 'is_approved', 'set', "tag")
