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


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('__all__')

class CreateTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'date_created')
