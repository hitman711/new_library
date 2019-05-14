from django.shortcuts import render, get_object_or_404

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

    def post(self, request, *args, **kwargs):
        """ """
        serializer = self.serializer_class(
            data=request.data,
            context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """ """
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
        else:
            serializer = self.serializer_class(
                data=request.data,
                context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """ """
        instance = self.get_object()
        serializer = self.serializer_class(
            instance,
            context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """ """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
