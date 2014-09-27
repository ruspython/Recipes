from django.shortcuts import render, HttpResponse, render_to_response, Http404, redirect, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.core.context_processors import csrf

from recipe.models import Recipe
from recipe.forms import RecipeForm
from random import randint


def get_random_recipe(recipes):
    return recipes[randint(0,len(recipes)-1)]


def home(request):
    args = {}
    if auth.get_user(request).is_authenticated():
        args['username'] = auth.get_user(request).username
    args['recipes'] = Recipe.objects.all()
    args['username'] = auth.get_user(request).username
    return render_to_response('home.html', args)


def recipe(request, recipe_id):
    args = {}
    if auth.get_user(request).is_authenticated():
        args['username'] = auth.get_user(request).username
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        args['recipe'] = recipe
        args['tags'] = recipe.tags.all()
    except ObjectDoesNotExist as e:
        raise Http404

    return render_to_response('recipe.html', args)


def addrecipe(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RecipeForm()
    if auth.get_user(request).is_authenticated():
        args['username'] = auth.get_user(request).username
        if request.POST:
            username = args['username']
            title = request.POST.get('title', 'fuck') #form.cleaned_data['title']
            text = request.POST.get('text', 'fuck') # form.clead_data['text']
            recipe = Recipe(author=username, title=title, text=text)
            recipe.save()
            return redirect('/recipes/'+str(recipe.id))
    else:
        return redirect('/auth/login/')
    return render_to_response('addrecipe.html', args, context_instance=RequestContext(request))


def searchbytag(request, tag_name):
    args = {}
    recipes = [recipe for recipe in Recipe.objects.all() for tag in recipe.tags.all() if tag_name in tag.name]
    args['recipes'] = recipes
    if auth.get_user(request).is_authenticated():
        args['username'] = auth.get_user(request).username
    args['tag_name'] = tag_name
    return render_to_response('serchbytag.html', args)