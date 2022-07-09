from rest_framework import serializers
from watchlist_app.models import Movie, Review, StreamPlatform

def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is too short!")
    return value

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ['movie',]
        
class MovieSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(queryset = StreamPlatform.objects.all(), slug_field='name')

    class Meta:
        model = Movie
        fields = '__all__'
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'