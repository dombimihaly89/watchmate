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
    # len_title = serializers.SerializerMethodField()
    platform = serializers.SlugRelatedField(queryset = StreamPlatform.objects.all(), slug_field='name')
    # reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ['active']
    
    # def get_len_title(self, object):
    #     return len(object.title)
        
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Title is too short!")
    #     return value
        
    # def validate(self, data):
    #     if data['title'] == data['storyline']:
    #         raise serializers.ValidationError("Title and storyline should be different!")
    #     return data
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    # movies = serializers.StringRelatedField(many=True)
    # movies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # movies = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-detail'
    # )
    movies = MovieSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short!")
#         return value
        
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and description should be different!")
#         return data