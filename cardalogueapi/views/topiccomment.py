# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
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

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            user = request.auth.user
            serializer = CreateTopicCommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(posted_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a topic_comments

        Returns:
            Response -- Empty body with 204 status code
        """
        topic_comment = TopicComment.objects.get(pk=pk)
        serializer = CreateTopicCommentSerializer(topic_comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for topic_comment
        Returns:
            Response -- empty body with 204 status code
        """
        try:
            topic_comment = TopicComment.objects.get(pk=pk)
            topic_comment.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except TopicComment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)



class TopicCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicComment
        fields = ('__all__')

class CreateTopicCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicComment
        fields = ('id', 'content', 'date', 'topic')
