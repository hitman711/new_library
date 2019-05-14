import unicodedata
import re
from django.db import models

from django.contrib.postgres.fields import JSONField
# Create your models here.


def slugify(value):
    value = unicodedata.normalize('NFKC', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


class Book(models.Model):
    """ Model to store Books information"""
    title = models.CharField(max_length=500)
    slug_name = models.SlugField(
        max_length=100,
        editable=False, blank=True, unique=True,
        help_text="Unique slug name slug name")
    publisher = models.CharField(max_length=300)
    author = models.CharField(max_length=255)
    pages = models.PositiveIntegerField(default=0)
    tags = JSONField(null=False, blank=True, default=[])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'books'
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return "%s (%s) published by %s" % (
            self.title, self.author, self.publisher)

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def tag_list(self):
        return []
