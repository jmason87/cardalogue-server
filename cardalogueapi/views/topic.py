# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from cardalogueapi.models import Topic

class TopicView(ViewSet):
    def list (self, request):
        """handes GET all"""
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET single"""
        topic = Topic.objects.get(pk=pk)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            user = request.auth.user
            serializer = CreateTopicSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk):
        """Handle PUT requests for a topic

        Returns:
            Response -- Empty body with 204 status code
        """
        topic = Topic.objects.get(pk=pk)
        serializer = CreateTopicSerializer(topic, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

        
    def destroy(self, request, pk):
        """Handle DELETE requests for topic
        Returns:
            Response -- empty body with 204 status code
        """
        try:
            topic = Topic.objects.get(pk=pk)
            topic.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Topic.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)



class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('__all__')

class CreateTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'date_created')
