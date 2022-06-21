from django.urls import path, include

# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import MovieListAV, MovieDetailAV, StreamPlatformListAV, StreamPlatformDetailAV

urlpatterns = [
    path('movie/list/', MovieListAV.as_view(), name='movie-list'),
    path('movie/<int:pk>', MovieDetailAV.as_view(), name='movie-detail'),
    path('streamplatform/list/', StreamPlatformListAV.as_view(), name='streamplatform-list'),
    path('streamplatform/<int:pk>', StreamPlatformDetailAV.as_view(), name='streamplatform-detail')
]
