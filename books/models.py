import unicodedata
import re
from django.db import models

from django.contrib.postgres.fields import JSONField
# Create your models here.


def slugify(value):
    """ Slugify book title"""
    if value:
        value = unicodedata.normalize('NFKC', value).strip().lower()
        return re.sub(r'[-\s]+', '-', value)
    return value

class Book(models.Model):
    """ Model to store Books information"""
    title = models.CharField(
        max_length=500, help_text="Book title")
    slug_name = models.SlugField(
        max_length=100,
        editable=False, blank=True, unique=True,
        help_text="Unique slug name slug name")
    publisher = models.CharField(
        max_length=300,
        help_text="Book publisher name")
    author = models.CharField(
        max_length=255,
        help_text="Book author name")
    pages = models.PositiveIntegerField(
        default=0,
        help_text="Total no. of pages in book")
    tags = JSONField(
        null=False, blank=True, default=[],
        help_text="List of tags")
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Book object creation date")
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Book object updation date")

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

