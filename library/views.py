from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.response import Response

from . import serializers


class Register(generics.CreateAPIView):
    """ """
    serializer_class = serializers.RegistrationSerializer
    model_class = serializer_class.Meta.model
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        operation_id="User Registrations",
        tags=['user'],
        request_body=serializer_class,
        responses={
            201: "{'message': 'User generated successfully'}"
        })
    def post(self, request, *args, **kwargs):
        """ API endpoint to authenticate & register user detail
        """
        return self.create(request, *args, **kwargs)


class Login(generics.GenericAPIView):
    """ """
    serializer_class = serializers.UserLoginSerializer
    model_class = serializer_class.Meta.model
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        operation_id="User Login",
        tags=['user'],
        request_body=serializer_class,
        responses={
            200: serializers.UserDetailSerializer
        })
    def post(self, request, *args, **kwargs):
        """ User Login
        
        API endpoint to authenticate and logged in user.

        All user have to login first to access authenticated API.
        """
        serializer = self.serializer_class(
            data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Logout(views.APIView):
    """ """
    @swagger_auto_schema(
        operation_id="User Logout",
        tags=['user'],
        responses={
            200: "{'message': 'User logged out successfully'}"
        })
    def post(self, request, *args, **kwargs):
        """ User Logout
        
        API endpoint to delete user authentication code and logged out from system
        """
        user = request.user
        token = user.auth_token
        token.delete()
        return Response(
            {'message': 'User logged out successfully'}, 
            status=status.HTTP_200_OK)
