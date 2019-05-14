
from django.shortcuts import get_object_or_404

from rest_framework.response import Response


class MultipleFieldLookupMixin(object):
    """
    View mixins to perform filter operation on model for
    retrieve data based on lookup field

    Parameters
    ----------
    lookup_fields : Tuple
        List of model parameters or search parameter
    lookup_url_kwargs : Tuple
        List of search data received from url to filter model information

      note :: Both lookup_fields, lookup_url_kwargs related to each other
        (i.e. In filter `lookup_fields` act as Key & `lookup_url_kwargs` act
        as Value)
    """

    def get_queryset(self, *args, **kwargs):
        """ Generate basic queryset based on URL view
            `select_related`, `prefetch_related` parameter pass from
            APIView
        """
        try:
            queryset = self.model_class.objects
            if self.select_related:
                queryset = queryset.select_related(*self.select_related)
            if self.prefetch_related:
                queryset = queryset.prefetch_related(*self.prefetch_related)
            queryset = queryset.all()
            return queryset
        except Exception as e:
            return self.model_class.objects.all()

    def get_object(self):
        """ Return single object
        """
        try:
            queryset = self.custom_query_class()
        except Exception as e:
            queryset = self.get_queryset()
        try:
            queryset = self.filter_queryset(queryset)
        except Exception as e:
            pass
        filter = {}
        # Field out `lookup_fields` and `lookup_url_kwargs` fields
        for field in self.lookup_fields:
            filter[field] = self.kwargs[
                self.lookup_url_kwargs[
                    self.lookup_fields.index(field)
                ]
            ]
        return get_object_or_404(queryset, **filter)

    def custom_lookup_filter(self, queryset):
        """ Add Filter value in queryset based on `lookup_fields` &
        `lookup_url_kwargs` fields
        """
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[
                self.lookup_url_kwargs[
                    self.lookup_fields.index(field)
                ]
            ]
        return queryset.filter(**filter)

    def list(self, *args, **kwargs):
        """ Return list objects based on queryset
        """
        try:
            queryset = self.filter_queryset(self.custom_query_class())
        except Exception as e:
            queryset = self.filter_queryset(self.get_queryset())
        queryset = self.custom_lookup_filter(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            try:
                self.stats(queryset)
            except Exception as e:
                pass
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
