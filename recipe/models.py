from django.db import models
from django import forms
from django.utils.safestring import mark_safe
import markdown

from recipe.util import urlize


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return '/recipes/searchbytag/%s/' % self.name



class Recipe(models.Model):
    author = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=200, verbose_name='Заголовок', null=False)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст', null=False)
    tags = models.ManyToManyField(Tag, null=False, help_text='')

    class Meta:
        ordering = ['-timestamp',]

    def get_absolute_url(self):
        return '/recipes/%s'%self.id

    def __str__(self):
        return self.title

    def get_content(self):
        content = mark_safe(urlize(markdown.markdown(self.text, safe_mode='escape')))
        content = content.replace('&lt;pre&gt;', '<pre>').replace(
            '&lt;code&gt;', '<code>').replace(
            '&lt;/code&gt;', '</code>').replace('&lt;/pre&gt;', '</pre>')
        return content
