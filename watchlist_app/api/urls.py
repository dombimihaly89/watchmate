from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api import views

router = DefaultRouter()
router.register('streamplatform', views.StreamPlatformMVS, basename='streamplatform')

urlpatterns = [
    path('movies', views.MovieListAV.as_view(), name='movie-list'),
    path('movies/<int:pk>', views.MovieDetailAV.as_view(), name='movie-detail'),
    path('movies/<int:pk>/reviews', views.ReviewList.as_view(), name='review-list'),
    path('movies/<int:pk>/reviews/create', views.ReviewCreate.as_view(), name='review-create'),
    path('', include(router.urls)),
    path('reviews/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),
    path('reviews', views.UserReview.as_view(), name='user-review')
]
