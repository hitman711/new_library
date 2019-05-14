from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        try:
            instance = super(
                RegistrationSerializer, self).create(validated_data)
            instance.set_password(validated_data['password'])
            instance.save()
            return instance
        except Exception as e:
            raise exceptions.APIException(
                'Service temporarily unavailable, try again later.'
            )

    def to_representation(self, instance):
        return {
            'message': 'User generated successfully'
        }


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, validated_data):
        """ """
        user = authenticate(
            request=self.context.get('request'),
            username=validated_data['username'],
            password=validated_data['password'])
        if user is None:
            raise serializers.ValidationError(
                'Invalid username and password'
            )
        Token.objects.get_or_create(user=user)
        self.instance = user
        return validated_data

    def to_representation(self, instance):
        """ """
        return UserDetailSerializer(instance).data


class UserDetailSerializer(serializers.ModelSerializer):
    """ """
    authentication_code = serializers.CharField(
        max_length=40, source='auth_token.key',
        help_text='API access key')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name',
            'last_name', 'authentication_code')
        read_only_fields = fields
