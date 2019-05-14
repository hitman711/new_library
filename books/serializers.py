from django.utils.text import slugify

from rest_framework import serializers

from . import models


class BookSerializer(serializers.ModelSerializer):
    """ Serializer to provide CRUD operation on Book model"""

    class Meta:
        model = models.Book
        fields = (
            'id', 'title', 'publisher', 'author', 'pages', 'tags',
            'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, validate_data):
        slug_value = models.slugify(validate_data['title'])
        if self.context['request'].method == 'POST':
            if models.Book.objects.filter(slug_name=slug_value).exists():
                raise serializers.ValidationError(
                    "Book name is already exists."
                )
        return validate_data
