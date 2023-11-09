from rest_framework import serializers

from advertisements.models import Advertisement, Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(read_only=True, source='owner.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'owner', 'advertisement']


class AdvertisementSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(read_only=True, source='owner.username')

    class Meta:
        model = Advertisement
        fields = ['id', 'text', 'owner', 'comments']
