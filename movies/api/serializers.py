from rest_framework import serializers

from ..models import Movie


class MovieSerializer(serializers.ModelSerializer):
    actors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'rating', 'actors']
