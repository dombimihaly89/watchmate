from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import (MovieListAV, MovieDetailAV, 
                                     ReviewDetail, StreamPlatformListAV, 
                                     StreamPlatformDetailAV, ReviewList, 
                                     # StreamPlatformViewSet,
                                     ReviewCreate,
                                     StreamPlatformMVS,
                                     UserReview)

router = DefaultRouter()
router.register('streamplatform', StreamPlatformMVS, basename='streamplatform')

urlpatterns = [
    path('movies', MovieListAV.as_view(), name='movie-list'),
    path('movies/<int:pk>', MovieDetailAV.as_view(), name='movie-detail'),
    path('movies/<int:pk>/reviews', ReviewList.as_view(), name='review-list'),
    path('movies/<int:pk>/reviews-create', ReviewCreate.as_view(), name='review-create'),
    #path('streamplatforms', StreamPlatformListAV.as_view(), name='streamplatform-list'),
    #path('streamplatforms/<int:pk>', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('', include(router.urls)),
    path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/', UserReview.as_view(), name='user-review')
]
