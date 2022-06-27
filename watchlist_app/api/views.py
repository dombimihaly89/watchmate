from asyncio import mixins
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser
from requests import Response, delete
from watchlist_app.models import Movie, Review, StreamPlatform
from watchlist_app.api.serializers import (MovieSerializer, ReviewSerializer,
                                           StreamPlatformSerializer)
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from watchlist_app.api.permissions import IsAdminOrReadonly, IsReviewUserOrAdminOrReadOnly
from functools import reduce

class MovieListAV(APIView):
    permission_classes = [IsAdminOrReadonly]
    
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class MovieDetailAV(APIView):
    permission_classes = [IsAdminOrReadonly]
    
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class StreamPlatformViewSet(viewsets.ViewSet):
    
#     def list(self,request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         streamplatform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(streamplatform)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def destroy(self, request, pk):
#         try:
#             streamplatform = StreamPlatform.objects.get(pk=pk)
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         streamplatform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformMVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadonly]
    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
class StreamPlatformListAV(APIView):
    
    def get(self, request):
        streamplatforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamplatforms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
class StreamPlatformDetailAV(APIView):
    
    def get(self, request, pk):
        try:
            streamplatform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(streamplatform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            streamplatform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(streamplatform, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        streamplatform = StreamPlatform.objects.get(pk=pk)
        streamplatform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movie=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserOrAdminOrReadOnly]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = ReviewSerializer
    
    def post(self, request, *args, **kwargs):
        if type(request.user) is AnonymousUser:
            return Response({'error': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = Movie.objects.get(pk=pk)
        
        author = self.request.user
        review_queryset = Review.objects.filter(movie=movie, author=author)
        
        if review_queryset.exists():
            raise ValidationError('You\'ve already reviewed this movie.')
        
        movie.number_of_ratings += 1
        reviews_on_movie = Review.objects.filter(movie=movie)
        if len(reviews_on_movie) == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            ratings_of_reviews = map(lambda m: m.rating, reviews_on_movie)
            sum_of_ratings = reduce(lambda a, b: a + b, ratings_of_reviews) + serializer.validated_data['rating']
            movie.avg_rating = sum_of_ratings / movie.number_of_ratings
        movie.save()
        
        serializer.save(movie=movie, author=author)
    
    def get_queryset(self):
        return Review.objects.all()
    

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(instance=movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)