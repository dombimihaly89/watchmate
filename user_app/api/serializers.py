from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
    def create(self, validated_data):
        password1 = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password1 != password2:
            raise serializers.ValidationError({'error': 'The passwords are different.'})
        
        users_with_same_email = User.objects.filter(email=self.validated_data['email'])
        if users_with_same_email.exists():
            raise serializers.ValidationError({'error': 'There is already a user with this email.'})
        
        account = User(email=validated_data['email'], username=validated_data['username'])
        account.set_password(password1)
        account.save()
        return account