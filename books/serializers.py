from django.utils.text import slugify

from rest_framework import serializers

from . import models


class BookSerializer(serializers.ModelSerializer):
    """ Serializer to provide CRUD operation on Book model"""
    tags = serializers.JSONField(
        default=[], help_text='List of tags')

    class Meta:
        model = models.Book
        fields = (
            'id', 'title', 'publisher', 'author', 'pages', 'tags',
            'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_tags(self, value):
        if value:
            if not isinstance(value, list):
                raise serializers.ValidationError(
                    "Tags should be list"
                )
        return value


    def validate_title(self, value):
        slug_value = models.slugify(value)
        if self.context['request'].method == 'POST':
            if models.Book.objects.filter(slug_name=slug_value).exists():
                raise serializers.ValidationError(
                    "Book title is already exists."
                )
        return value
