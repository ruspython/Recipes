from django.shortcuts import render, HttpResponse, render_to_response, Http404, redirect, RequestContext, \
    get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.utils.timezone import now
from django.core.paginator import Paginator

from recipe.models import Recipe
from recipe.forms import RecipeForm
from random import randint


def get_random_recipe(recipes):
    return recipes[randint(0, len(recipes) - 1)]


def home(request, page_number=1):
    args = {}
    recipes = Recipe.objects.all()
    cur_page = Paginator(recipes, 7)
    if auth.get_user(request).is_authenticated():
        args['username'] = auth.get_user(request).username
    args['recipes'] = cur_page.page(page_number)
    args['username'] = auth.get_user(request).username
    return render_to_response('home.html', args)


def searchbytag(request, tag_name, page_number=1):
    args = {}
    recipes = [recipe for recipe in Recipe.objects.all() for tag in recipe.tags.all() if tag_name in tag.name]
    cur_page = Paginator(recipes, 7)
    args['recipes'] = cur_page.page(page_number)
    if auth.get_user(request).is_authenticated():
        args['username'] = auth.get_user(request).username
    args['tag_name'] = tag_name
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
            form = RecipeForm(request.POST)
            if form.is_valid():
                recipe = form.save()
                return redirect('/recipes/' + str(recipe.id))
            args['form'] = form
    else:
        return redirect('/auth/login/')
    return render_to_response('addrecipe.html', args, context_instance=RequestContext(request))


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    args = {}
    args['recipe'] = recipe
    args['form'] = form = RecipeForm(request.POST or None, instance=recipe)
    args['username'] = username = auth.get_user(request).username
    user = auth.get_user(request)
    if not user.is_superuser:
        if not user.username == recipe.author:
            return redirect('/auth/login/')
    if form.is_valid():
        # form = RecipeForm(request.POST)
        recipe = form.save(commit=False)

        recipe.timestamp = now()

        recipe.save()
        form.save_m2m()
        print('saving')

        return redirect('/recipes/' + str(recipe.id))
    print('just enter')
    return render_to_response('editrecipe.html', args, context_instance=RequestContext(request))