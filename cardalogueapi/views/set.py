# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
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

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            serializer = CreateSetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE requests for set
        Returns:
            Response -- empty body with 204 status code
        """
        try:
            single_set = Set.objects.get(pk=pk)
            single_set.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Set.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('__all__')

class CreateSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('id', 'name', 'manufacturer', 'year')
