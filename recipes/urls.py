from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^recipe/add', 'recipe.views.addrecipe'),
    url(r'^recipes/searchbytag/(?P<tag_name>.+)/(\d+)', 'recipe.views.searchbytag'),
    url(r'^recipes/searchbytag/(?P<tag_name>.+)', 'recipe.views.searchbytag'),
    url(r'^recipes/(?P<recipe_id>\d+)', 'recipe.views.recipe', name='recipe'),
    url(r'^recipes/editrecipe/(?P<recipe_id>\d+)', 'recipe.views.edit_recipe'),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^page/(\d+)', 'recipe.views.home'),
    url(r'^getdate', 'recipe.views.getdate'),
    url(r'^$', 'recipe.views.home', name='home_page'),

    # Flat pages
    url(r'', include('django.contrib.flatpages.urls')),

)
