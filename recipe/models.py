from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Recipe(models.Model):
    author = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=200, verbose_name='Заголовок', null=False)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст', null=False)
    tags = models.ManyToManyField(Tag, null=False, help_text='')

    def __str__(self):
        return self.title
