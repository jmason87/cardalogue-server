# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cardalogueapi.models import TopicComment

class TopicCommentView(ViewSet):
    def list (self, request):
        """handes GET all"""
        topic_comments = TopicComment.objects.all()
        serializer = TopicCommentSerializer(topic_comments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET single"""
        topic_comment = TopicComment.objects.get(pk=pk)
        serializer = TopicCommentSerializer(topic_comment)
        return Response(serializer.data)

class TopicCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicComment
        fields = ('__all__')
