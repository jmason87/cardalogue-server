# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from cardalogueapi.models import CollectionComment

class CollectionCommentView(ViewSet):
    def list (self, request):
        """handes GET all"""
        comments = CollectionComment.objects.all()
        serializer = CollectionCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET single"""
        comment = CollectionComment.objects.get(pk=pk)
        serializer = CollectionCommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            user = request.auth.user
            serializer = CreateCollectionCommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(posted_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a collection_comments

        Returns:
            Response -- Empty body with 204 status code
        """
        collection_comment = CollectionComment.objects.get(pk=pk)
        serializer = CreateCollectionCommentSerializer(collection_comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for collection_comment
        Returns:
            Response -- empty body with 204 status code
        """
        try:
            collection_comment = CollectionComment.objects.get(pk=pk)
            collection_comment.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except CollectionComment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class CollectionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionComment
        fields = ('__all__')
        depth = 1

class CreateCollectionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionComment
        fields = ('id', 'content', 'date', 'collection')
