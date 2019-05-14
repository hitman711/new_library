from rest_framework import generics, status
from rest_framework.response import Response

from . import serializers


class Register(generics.CreateAPIView):
    """ """
    serializer_class = serializers.RegistrationSerializer
    model_class = serializer_class.Meta.model
    authentication_classes = ()
    permission_classes = ()


class Login(generics.GenericAPIView):
    """ """
    serializer_class = serializers.UserLoginSerializer
    model_class = serializer_class.Meta.model
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """ API endpoint to authenticate and logged in user.
        All user have to login first to access authenticated API.
        """
        serializer = self.serializer_class(
            data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Logout(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        """ """
        user = request.user
        token = user.auth_token
        token.delete()
        return Response({'message': 'User logged out successfully'})
