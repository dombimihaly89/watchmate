from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import logout_view, registration_view
from django.urls import path

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout')
]
