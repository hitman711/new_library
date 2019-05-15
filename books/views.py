from django.shortcuts import render, get_object_or_404

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from library import mixins
from . import serializers
from .models import slugify
# Create your views here.


class BookView(generics.GenericAPIView):
    """ """
    serializer_class = serializers.BookSerializer
    model_class = serializer_class.Meta.model
    queryset = model_class.objects.all()

    def get_object(self):
        """ Return single object
        """
        queryset = self.get_queryset().all()
        filter = {}
        # Field out `lookup_fields` and `lookup_url_kwargs` fields
        slug_name = slugify(self.request.GET.get('title'))
        if slug_name:
            filter['slug_name'] = slug_name
        else:
            filter['slug_name'] = self.request.GET.get('title')
        return get_object_or_404(queryset, **filter)

    @swagger_auto_schema(
        operation_id="Create book detail",
        tags=['book'],
        request_body=serializer_class,
        responses={
            201: serializer_class,
            400: '{"title":"Book title is already exists."}'
        })
    def post(self, request, *args, **kwargs):
        """ Create book detail

        API endpoint to create new book detail
        """
        serializer = self.serializer_class(
            data=request.data,
            context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_id="Create/Update book detail",
        tags=['book'],
        request_body=serializer_class,
        responses={
            201: serializer_class,
            200: serializer_class
        })
    def put(self, request, *args, **kwargs):
        """ Create / Update book detail
        
        API endpoint to create/update book details.
        
        Check book object available in database using title from 
        request data. If it's available the update existing object
        and return response 200. If not then create new object
        and return response 201.
        """
        queryset = self.get_queryset()
        instance = None
        if self.request.data.get('title'):
            slug_name = slugify(self.request.data.get('title'))
            if slug_name:
                instance = queryset.filter(
                    slug_name=slug_name
                ).last()
            else:
                instance = queryset.filter(
                    slug_name=self.request.data.get('title')
                ).last()
        if instance:
            serializer = self.serializer_class(
                instance=instance,
                data=request.data,
                context=self.get_serializer_context())
            return_status = status.HTTP_200_OK
        else:
            serializer = self.serializer_class(
                data=request.data,
                context=self.get_serializer_context())
            return_status = status.HTTP_201_CREATED
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=return_status)

    @swagger_auto_schema(
        operation_id="Get book detail",
        tags=['book'],
        manual_parameters=[
            openapi.Parameter(
                'title', openapi.IN_QUERY, 
                "Get book detail using title", 
                type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: serializer_class,
            404:'{"detail":"Not found"}'
        })
    def get(self, request, *args, **kwargs):
        """ Book Detail
        
        Fetch book detail using title query parameter
        """
        instance = self.get_object()
        serializer = self.serializer_class(
            instance,
            context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="Delete book detail",
        tags=['book'],
        manual_parameters=[
            openapi.Parameter(
                'title', openapi.IN_QUERY, 
                "Get book detail using title", 
                type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            204: 'NO CONTENT',
            404:'{"detail": "Not found."}'
        })
    def delete(self, request, *args, **kwargs):
        """ Detail book detail
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
