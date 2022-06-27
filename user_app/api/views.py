from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
# from user_app import models

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
    print(token)
    data['token'] = token
    return Response(data)

@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)