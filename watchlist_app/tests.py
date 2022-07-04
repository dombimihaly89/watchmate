from platform import platform
from django.contrib.auth.models import User
from django.urls import reverse
from django.forms.models import model_to_dict

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatfromTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_superuser(username='example', password='PassWord@123')
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        streamplatform1 = models.StreamPlatform(name='Netflix', about='Good platform', website='https://www.netflix.com')
        streamplatform2 = models.StreamPlatform(name='HBO go', about='Nice platform', website='https://www.hbo.com')
        streamplatforms = [streamplatform1, streamplatform2]
        
        self.streamplatforms = models.StreamPlatform.objects.bulk_create(streamplatforms)
    
    def test_streamplatform_create(self):
        data = {
            'name': 'Netflix',
            'about': 'Good platform',
            'website': 'https://netflix.com'
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        response.data['movies'] = tuple(response.data['movies'])
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(set(data.items()).issubset(set(response.data.items())))
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        for index, data in enumerate(response.data):
            data['movies'] = tuple(data['movies'])
            self.assertTrue(set(model_to_dict(self.streamplatforms[index]).items()).issubset(set(data.items())))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.streamplatforms[0].id,)))
        response.data['movies'] = tuple(response.data['movies'])
        self.assertTrue(set(model_to_dict(self.streamplatforms[0]).items()).issubset(set(response.data.items())))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class MovieTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_superuser(username = 'example', password = 'password')
        self.token = Token.objects.get(user__username = self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        self.streamplatform = models.StreamPlatform.objects.create(name='Netflix', about='Good platform', website='https://www.netflix.com')
        movie1 = models.Movie(title='Spiderman', storyline='Some movie', platform=self.streamplatform, active=True)
        movie2 = models.Movie(title='Batman', storyline='Some bat movie', platform=self.streamplatform, active=True)
        movies = [movie1, movie2]
        
        self.movies = models.Movie.objects.bulk_create(movies)
    
    def test_movie_create(self):
        data = {
            'platform': self.streamplatform.name,
            'title': 'Batman',
            'storyline': 'About some bat who is a man',
            'active': True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertTrue(set(data.items()).issubset(set(response.data.items())))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_movie_list(self):
        response = self.client.get(reverse('movie-list'))
        for index, data in enumerate(response.data):
            movie = model_to_dict(self.movies[index])
            movie['platform'] = self.movies[index].platform.name
            self.assertTrue(set(movie.items()).issubset(set(data.items())))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_movie_detail(self):
        movie = model_to_dict(self.movies[0])
        movie['platform'] = self.movies[0].platform.name
        response = self.client.get(reverse('movie-detail', args=(movie['id'],)))
        self.assertTrue(set(movie.items()).issubset(set(response.data.items())))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class ReviewTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username = 'example', password = 'password')
        self.token = Token.objects.get(user__username = self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        self.streamplatform = models.StreamPlatform.objects.create(name='Netflix', about='Good platform', website='https://www.netflix.com')
        self.movie = models.Movie.objects.create(title='Spiderman', storyline='Some movie', platform=self.streamplatform, active=True)
    
    def test_review_create(self):
        data = {
            'author': self.user,
            'rating': 5,
            'description': 'Great movie',
            'movie': self.movie,
            'active': True
        }
        
        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 1)
        self.assertEqual(models.Review.objects.get().rating, 5)
        
        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauth(self):
        data = {
            'author': self.user,
            'rating': 5,
            'description': 'Great movie',
            'movie': self.movie,
            'active': True
        }
        
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        self.review = models.Review.objects.create(author = self.user, rating = 5, description = 'Great movie', movie = self.movie, active = True)
        data = {
            'author': self.user,
            'rating': 4,
            'description': 'Great movie',
            'movie': self.movie,
            'active': True
        }
        
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], data['rating'])
        
    def test_review_list(self):
        self.review = models.Review.objects.create(author = self.user, rating = 5, description = 'Great movie', movie = self.movie, active = True)
        self.client.force_authenticate(user=None)
        user2 = User.objects.create_user(username = 'example2', password = 'password')
        self.token = Token.objects.get(user__username = self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        self.review = models.Review.objects.create(author = user2, rating = 5, description = 'Great movie', movie = self.movie, active = True)
        
        response = self.client.get(reverse('review-list', args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_review_detail(self):
        self.review = models.Review.objects.create(author = self.user, rating = 5, description = 'Great movie', movie = self.movie, active = True)
        
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.review.description)
        
    def test_review_delete(self):
        self.review = models.Review.objects.create(author = self.user, rating = 5, description = 'Great movie', movie = self.movie, active = True)
        
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Review.objects.count(), 0)
     
        
class UserReviewTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username = 'example', password = 'password')
        self.token = Token.objects.get(user__username = self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.streamplatform = models.StreamPlatform.objects.create(name='Netflix', about='Good platform', website='https://www.netflix.com')
        self.movie1 = models.Movie.objects.create(title='Spiderman', storyline='Some movie', platform=self.streamplatform, active=True)
        self.movie2 = models.Movie.objects.create(title='Batman', storyline='Some movie', platform=self.streamplatform, active=True)
        
        self.review1 = models.Review.objects.create(author = self.user, rating = 5, description = 'Great movie', movie = self.movie1, active = True)
        self.review2 = models.Review.objects.create(author = self.user, rating = 5, description = 'Great movie', movie = self.movie2, active = True)
    
    def test_user_review(self):
        response = self.client.get('/api/reviews?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        
        
    
    

