from functools import reduce

from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from watchlist_app.api import pagination, permissions, serializers

from watchlist_app import models


class MovieListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadonly]
    
    def get(self, request):
        movies = models.Movie.objects.all()
        serializer = serializers.MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class MovieDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadonly]
    
    def get(self, request, pk):
        try:
            movie = models.Movie.objects.get(pk=pk)
        except models.Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.MovieSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = models.Movie.objects.get(pk=pk)
        serializer = serializers.MovieSerializer(movie, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = models.Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformMVS(viewsets.ModelViewSet):
    queryset = models.StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadonly]
    
class ReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active']
    search_fields = ['author__username']
    pagination_class = pagination.ReviewCursorPagination
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(movie=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsReviewUserOrAdminOrReadOnly]
    throttle_scope = 'review-detail'

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    
class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = serializers.ReviewSerializer
    
    def post(self, request, *args, **kwargs):
        if type(request.user) is AnonymousUser:
            return Response({'error': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = models.Movie.objects.get(pk=pk)
        
        author = self.request.user
        review_queryset = models.Review.objects.filter(movie=movie, author=author)
        
        if review_queryset.exists():
            raise ValidationError('You\'ve already reviewed this movie.')
        
        movie.number_of_ratings += 1
        reviews_on_movie = models.Review.objects.filter(movie=movie)
        if len(reviews_on_movie) == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            ratings_of_reviews = map(lambda m: m.rating, reviews_on_movie)
            sum_of_ratings = reduce(lambda a, b: a + b, ratings_of_reviews) + serializer.validated_data['rating']
            movie.avg_rating = sum_of_ratings / movie.number_of_ratings
        movie.save()
        
        serializer.save(movie=movie, author=author)
    
    def get_queryset(self):
        return models.Review.objects.all()
    
class UserReview(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ReviewSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        reviews = models.Review.objects.filter(author__username=username)
        
        return reviews