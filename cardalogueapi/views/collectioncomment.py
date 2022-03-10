# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
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

class CollectionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionComment
        fields = ('__all__')
