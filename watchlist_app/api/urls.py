from django.urls import path, include

# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import MovieListAV, MovieDetailAV, ReviewDetail, StreamPlatformListAV, StreamPlatformDetailAV, ReviewList

urlpatterns = [
    path('movies', MovieListAV.as_view(), name='movie-list'),
    path('movies/<int:pk>', MovieDetailAV.as_view(), name='movie-detail'),
    path('movies/<int:pk>/reviews', ReviewList.as_view(), name='review-list'),
    path('streamplatforms', StreamPlatformListAV.as_view(), name='streamplatform-list'),
    path('streamplatforms/<int:pk>', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail')
]
