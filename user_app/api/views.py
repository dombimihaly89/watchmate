from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user_app import models

@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    serializer.is_valid(raise_exception=True)
    account = serializer.save()
    data['message'] = 'Registration Successful!'
    data['username'] = account.username
    data['email'] = account.email
    token = Token.objects.get_or_create(user=account)[0].key
    data['token'] = token
    # data['token'] = get_tokens_for_user(account)
    return Response(data)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
