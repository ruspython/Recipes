from django.contrib import admin

from .models import Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    fields = ['name',]


class RecipeAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'text', 'tags',]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
# Register your models here.
